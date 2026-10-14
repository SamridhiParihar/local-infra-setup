# Chapter 1 — Local AI Infrastructure Fundamentals

## What it means

Local agentic infrastructure is the hardware and software needed to run a model on a local computer or lab machine, connect it to tools and data, and build programs that use it to work toward a goal. “Local” refers to where inference happens: an application running on a laptop may still send requests to a cloud model.

A **model** generates outputs. An **agent** is program logic that uses a model, may call tools, and decides what to do next. A model running locally is not automatically an agent.

## Main layers

1. **Hardware** — CPU, GPU, memory, and storage.
2. **Model** — learned weights, such as an LLM or VLM.
3. **Runtime** — loads the weights and computes outputs.
4. **Model interface** — lets another program send inputs and receive outputs.
5. **Agent logic** — chooses steps and may call tools.
6. **Data and memory** — information the system can retrieve or retain.
7. **Measurement** — latency, throughput, and resource use.

For robotics, these layers eventually connect to sensors, perception, planning, robot software, controllers, and hardware.

## First experiment

Start with a small text model and a local runtime. Record the machine, runtime and version, model and format, model file size, prompt, response time, and memory use. Repeat the same prompt to build a baseline.

## Key distinctions

- **Inference** runs a trained model to produce an output.
- **Runtime** is the software that loads and runs the model.
- **Model weights** are learned numerical parameters stored in files.
- **Local API** is an interface another program can call on the same machine.
- **VLM** means a model that can process images as well as text.

## Takeaway

Keep the layers separate when debugging. Poor answers may come from the model, prompt, or agent logic. Slow responses may come from model size, runtime, memory pressure, or hardware. A repeatable baseline helps distinguish these causes.
