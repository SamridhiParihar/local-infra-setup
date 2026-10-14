# Experiment 01 — Run a Small Local LLM

## Objective

Run a text model locally, confirm which runtime and model are involved, and record a first baseline on the MacBook Pro with Apple M1 Pro.

## Setup

| Item | Value |
|---|---|
| Operating system | macOS (version to record) |
| Hardware | Apple M1 Pro MacBook Pro |
| Installed RAM | To record |
| Inference runtime | Ollama |
| Runtime version | 0.40.3 |
| Model | `qwen3:0.6b` |
| Model file size | 522 MB (reported by `ollama pull`) |
| Model download rate | 4.1 MB/s over mobile hotspot |

## Automated run command

From the repository root, run:

```bash
python3 tools/run_ollama_experiment.py --model qwen3:0.6b --prompt "Explain the difference between an LLM and an agent in three bullet points."
```

`python3` runs the local script, `--model` selects the already-downloaded Ollama model, and `--prompt` supplies the text to measure. The script calls only `http://127.0.0.1:11434/api` on this Mac and appends one row to [`results.csv`](results.csv).

It records host and runtime details, model size and metadata, prompt and response, time to the first output chunk, Ollama's model-load and prompt/generation timings, token counts, generated tokens per second, and an `ollama ps` snapshot. The first streamed text chunk is a useful latency measure but is not guaranteed to equal the exact first-token time.

Ollama's API does not return a complete GPU/CPU utilization or peak-memory time series. We will add a separate resource sampler when the experiment reaches hardware measurement; for now, use the saved `ollama ps` snapshot and add any Activity Monitor observations to the notes below.

## Procedure

1. Confirm the Ollama CLI runs and record its version.
2. Download a small text model and record the exact model tag.
3. Run the fixed prompt with the automated runner.
4. Review the automatically recorded timings and token counts.
5. Repeat with the same prompt and compare runs.

## Prompt

> Explain the difference between a model and an agent in three bullet points.

## Results

Not run yet.

See [`results.csv`](results.csv) for the measurement log.

## Notes and issues

### Setup and download observations (12 October 2026)

- Ollama installer download on IIITH Wi-Fi took 1 hour 48 minutes.
- `networkQuality` reported 20.934 Mbps downlink and 147.897 Mbps uplink.
- A capped 5 MiB request to the Ollama download URL over IIITH Wi-Fi received 1,828,177 bytes in 60.24 seconds (about 30 KB/s).
- The same capped request over a mobile hotspot received 5,242,880 bytes in 2.44 seconds (about 2.1 MB/s).
- The `qwen3:0.6b` model download completed over the hotspot at 4.1 MB/s.

This points to the IIITH Wi-Fi path as the bottleneck for the tested Ollama download, though it does not establish whether the cause is local congestion, network policy, or routing. Add inference observations here after running the prompt.
