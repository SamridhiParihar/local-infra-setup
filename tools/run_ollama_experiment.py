#!/usr/bin/env python3
"""Run a prompt against a local Ollama model and append a measurement row."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import platform
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


API_ROOT = "http://127.0.0.1:11434/api"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = REPO_ROOT / "experiments" / "01-small-local-llm" / "results.csv"

FIELDS = [
    "timestamp_local",
    "host_name",
    "operating_system",
    "architecture",
    "chip",
    "installed_ram_bytes",
    "runtime",
    "runtime_version",
    "api_endpoint",
    "model_tag",
    "model_file_size_bytes",
    "model_parameter_size",
    "model_quantization",
    "model_format",
    "model_family",
    "model_context_length_tokens",
    "model_store_path",
    "generation_options_json",
    "prompt",
    "response",
    "time_to_first_output_chunk_seconds",
    "client_request_seconds",
    "server_total_seconds",
    "model_load_seconds",
    "prompt_token_count",
    "prompt_eval_seconds",
    "output_token_count",
    "generation_seconds",
    "generation_tokens_per_second",
    "done_reason",
    "ollama_ps_snapshot",
    "server_metrics_json",
]


def request_json(path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{API_ROOT}/{path}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="GET" if data is None else "POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def command_output(command: list[str], timeout: int = 10) -> str:
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {exc}"
    return "\n".join(part for part in (completed.stdout.strip(), completed.stderr.strip()) if part)


def installed_ram_bytes() -> str:
    if platform.system() != "Darwin":
        return ""
    value = command_output(["sysctl", "-n", "hw.memsize"])
    return value if value.isdigit() else ""


def ollama_version() -> str:
    raw = command_output(["ollama", "--version"])
    match = re.search(r"client version is\s+([^\s]+)", raw, re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r"(?:version\s+)?v?\d+\.\d+\.\d+", raw, re.IGNORECASE)
    return match.group(0) if match else raw


def seconds_from_ns(value: Any) -> str:
    try:
        return f"{int(value) / 1_000_000_000:.6f}"
    except (TypeError, ValueError):
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run and record one prompt using the local Ollama API."
    )
    parser.add_argument("--model", default="qwen3:0.6b", help="Local Ollama model tag")
    parser.add_argument("--prompt", required=True, help="Prompt text to send")
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Optional generation temperature; omitted means use the model default",
    )
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="CSV log path")
    args = parser.parse_args()

    options: dict[str, Any] = {}
    if args.temperature is not None:
        options["temperature"] = args.temperature

    try:
        tags = request_json("tags")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(
            "Could not reach the local Ollama API at http://127.0.0.1:11434. "
            "Check that the Ollama app is running.",
            file=sys.stderr,
        )
        print(f"Details: {exc}", file=sys.stderr)
        return 1

    models = tags.get("models", [])
    model_entry = next(
        (entry for entry in models if entry.get("name") == args.model or entry.get("model") == args.model),
        {},
    )
    try:
        show = request_json("show", {"model": args.model})
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        show = {}
    details = show.get("details", {})

    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "stream": True,
    }
    if options:
        payload["options"] = options

    print(f"Model: {args.model} (local API: {API_ROOT})")
    print("Response:")

    request_start = time.perf_counter()
    first_output_at: float | None = None
    response_parts: list[str] = []
    final_event: dict[str, Any] = {}
    request = urllib.request.Request(
        f"{API_ROOT}/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=600) as stream:
            for line in stream:
                if not line.strip():
                    continue
                event = json.loads(line.decode("utf-8"))
                chunk = event.get("response", "")
                if chunk:
                    if first_output_at is None:
                        first_output_at = time.perf_counter()
                    response_parts.append(chunk)
                    print(chunk, end="", flush=True)
                if event.get("done"):
                    final_event = event
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"\nRequest failed: {exc}", file=sys.stderr)
        return 1

    client_seconds = time.perf_counter() - request_start
    print("\n")
    ps_snapshot = command_output(["ollama", "ps"])

    eval_count = final_event.get("eval_count", "")
    eval_duration = final_event.get("eval_duration", "")
    try:
        tokens_per_second = f"{int(eval_count) / (int(eval_duration) / 1_000_000_000):.3f}"
    except (TypeError, ValueError, ZeroDivisionError):
        tokens_per_second = ""

    first_output_seconds = (
        f"{first_output_at - request_start:.6f}" if first_output_at is not None else ""
    )
    model_info = show.get("model_info", {})
    family = details.get("family", "")
    families = details.get("families", [])
    if not family and families:
        family = ",".join(families)
    context_length = next(
        (value for key, value in model_info.items() if key.endswith("context_length")),
        "",
    )

    row = {
        "timestamp_local": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "host_name": platform.node(),
        "operating_system": f"{platform.system()} {platform.release()} {platform.mac_ver()[0]}".strip(),
        "architecture": platform.machine(),
        "chip": command_output(["sysctl", "-n", "machdep.cpu.brand_string"])
        if platform.system() == "Darwin"
        else platform.processor(),
        "installed_ram_bytes": installed_ram_bytes(),
        "runtime": "Ollama",
        "runtime_version": ollama_version(),
        "api_endpoint": API_ROOT,
        "model_tag": args.model,
        "model_file_size_bytes": model_entry.get("size", ""),
        "model_parameter_size": details.get("parameter_size", ""),
        "model_quantization": details.get("quantization_level", ""),
        "model_format": details.get("format", ""),
        "model_family": family,
        "model_context_length_tokens": context_length,
        "model_store_path": str(Path.home() / ".ollama" / "models"),
        "generation_options_json": json.dumps(options, sort_keys=True),
        "prompt": args.prompt,
        "response": "".join(response_parts),
        "time_to_first_output_chunk_seconds": first_output_seconds,
        "client_request_seconds": f"{client_seconds:.6f}",
        "server_total_seconds": seconds_from_ns(final_event.get("total_duration")),
        "model_load_seconds": seconds_from_ns(final_event.get("load_duration")),
        "prompt_token_count": final_event.get("prompt_eval_count", ""),
        "prompt_eval_seconds": seconds_from_ns(final_event.get("prompt_eval_duration")),
        "output_token_count": eval_count,
        "generation_seconds": seconds_from_ns(eval_duration),
        "generation_tokens_per_second": tokens_per_second,
        "done_reason": final_event.get("done_reason", ""),
        "ollama_ps_snapshot": ps_snapshot,
        "server_metrics_json": json.dumps(final_event, sort_keys=True),
    }

    args.log.parent.mkdir(parents=True, exist_ok=True)
    write_header = not args.log.exists() or args.log.stat().st_size == 0
    with args.log.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print("Run summary:")
    print(f"  First output chunk: {first_output_seconds or 'not measured'} s")
    print(f"  Model load: {row['model_load_seconds'] or 'not reported'} s")
    print(f"  Output tokens: {eval_count or 'not reported'}")
    print(f"  Generation speed: {tokens_per_second or 'not reported'} tokens/s")
    print(f"  Log appended to: {args.log}")
    if model_info:
        print("  Model metadata was read from the local Ollama server.")
    print("  Memory/GPU utilization needs a separate sampler; it is not claimed here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
