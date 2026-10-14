# Local Agentic Infrastructure

A practical learning and research log for running local LLMs and VLMs, measuring their resource use, and gradually connecting them to agent and robotics systems.

## Learning workflow

For each topic, follow:

**Understand → Run → Measure → Break → Debug → Optimize → Document**

Keep experiment inputs and measurements here so that results can be repeated. Do not commit downloaded model weights, credentials, or private keys.

## Current machine

- MacBook Pro with Apple M1 Pro
- macOS
- RAM capacity: record from **Apple menu → About This Mac**
- Other environments: Ubuntu/ Linux and UTM are available; record their configurations separately

## Roadmap

1. Local AI infrastructure fundamentals
2. LLM and VLM model basics
3. Model formats and quantization
4. Local inference runtimes
5. Hardware and memory requirements
6. Benchmarking
7. Agent infrastructure and tools
8. Containers, CUDA, and remote compute
9. Edge and robotics integration

## Experiments

- [01 — Run a small local LLM](experiments/01-small-local-llm/README.md)
- Automated prompt runner: [`tools/run_ollama_experiment.py`](tools/run_ollama_experiment.py)

## Notes

- [Chapter 1 — Local AI infrastructure fundamentals](chapters/01-local-ai-infrastructure.md)
- [Chapter 2 — LLM and VLM model basics](chapters/02-llm-vlm-model-basics.md)
- [References](references/sources.md)
