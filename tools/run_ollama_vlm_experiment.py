#!/usr/bin/env python3
"""Send one local image-and-text prompt to Ollama and record the run."""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


API_ROOT = "http://127.0.0.1:11434/api"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = REPO_ROOT / "experiments" / "02-local-vlm" / "results.csv"
FIELDS = [
    "timestamp_local",
    "host_name",
    "operating_system",
    "architecture",
    "installed_ram_bytes",
    "runtime",
    "runtime_version",
    "model_tag",
    "model_size_bytes",
    "model_parameter_size",
    "model_quantization",
    "image_path",
    "image_size_bytes",
    "image_sha256",
    "image_dimensions",
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


def command_output(command: list[str], timeout: int = 10) -> str:
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {exc}"
    return "\n".join(
        part for part in (result.stdout.strip(), result.stderr.strip()) if part
    )


def request_json(path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{API_ROOT}/{path}",
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="GET" if data is None else "POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def seconds_from_ns(value: Any) -> str:
    try:
        return f"{int(value) / 1_000_000_000:.6f}"
    except (TypeError, ValueError):
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Send one image and prompt to a local Ollama vision model."
    )
    parser.add_argument("--model", default="qwen3-vl:2b", help="Local Ollama model tag")
    parser.add_argument("--image", required=True, type=Path, help="Image file to send")
    parser.add_argument("--prompt", required=True, help="Question about the image")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="CSV log path")
    args = parser.parse_args()

    if not args.image.is_file():
        print(f"Image file not found: {args.image}", file=sys.stderr)
        return 2

    image_bytes = args.image.read_bytes()
    image_base64 = base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": args.prompt,
                "images": [image_base64],
            }
        ],
        "stream": True,
        # Ollama reports this model's thinking mode as enabled by default.
        # Disable it here so the experiment records a user-facing answer.
        "think": False,
    }

    try:
        tags = request_json("tags")
        show = request_json("show", {"model": args.model})
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(
            "Could not reach the local Ollama API at http://127.0.0.1:11434. "
            "Check that the Ollama app is running.",
            file=sys.stderr,
        )
        print(f"Details: {exc}", file=sys.stderr)
        return 1

    model_entry = next(
        (
            entry
            for entry in tags.get("models", [])
            if entry.get("name") == args.model or entry.get("model") == args.model
        ),
        {},
    )
    details = show.get("details", {})

    image_dimensions = ""
    if platform.system() == "Darwin":
        image_dimensions = command_output(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(args.image)]
        )

    print(f"Model: {args.model} (local API: {API_ROOT})")
    print(f"Image: {args.image} ({len(image_bytes)} bytes)")
    print("Response:")

    request = urllib.request.Request(
        f"{API_ROOT}/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    request_start = time.perf_counter()
    first_output_at: float | None = None
    response_parts: list[str] = []
    thinking_was_returned = False
    final_event: dict[str, Any] = {}

    try:
        with urllib.request.urlopen(request, timeout=600) as stream:
            for line in stream:
                if not line.strip():
                    continue
                event = json.loads(line.decode("utf-8"))
                message = event.get("message", {})
                if message.get("thinking"):
                    thinking_was_returned = True
                chunk = message.get("content", "")
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
    if not response_parts:
        if thinking_was_returned:
            print("Ollama sent thinking text, but no answer text.")
        else:
            print("Ollama returned no answer text.")
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
    row = {
        "timestamp_local": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "host_name": platform.node(),
        "operating_system": f"{platform.system()} {platform.release()} {platform.mac_ver()[0]}".strip(),
        "architecture": platform.machine(),
        "installed_ram_bytes": command_output(["sysctl", "-n", "hw.memsize"])
        if platform.system() == "Darwin"
        else "",
        "runtime": "Ollama",
        "runtime_version": command_output(["ollama", "--version"]),
        "model_tag": args.model,
        "model_size_bytes": model_entry.get("size", ""),
        "model_parameter_size": details.get("parameter_size", ""),
        "model_quantization": details.get("quantization_level", ""),
        "image_path": str(args.image.expanduser().resolve()),
        "image_size_bytes": len(image_bytes),
        "image_sha256": hashlib.sha256(image_bytes).hexdigest(),
        "image_dimensions": image_dimensions,
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
    print(f"  Stop reason: {final_event.get('done_reason', 'not reported')}")
    print(f"  Log appended to: {args.log}")
    print("  Memory/GPU utilization needs a separate sampler; it is not claimed here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
