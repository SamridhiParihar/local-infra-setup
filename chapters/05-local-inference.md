# Chapter 5 — Local Inference

## 1. What inference means

**Inference** is when a trained model uses its learned weights to produce an answer. The model is not being trained or changed; we are using it.

When our Python script sent a prompt to `qwen3:0.6b` and received a response, it was running inference locally.

## 2. The three main parts

- **Model:** the learned weights and related model data, stored on the computer.
- **Inference runtime:** software that loads the model and runs its calculations on the computer's CPU or GPU.
- **App or script:** sends a prompt to the runtime and handles the response.

The model contains the learned information. The runtime is the software that uses it.

## 3. What happens during a request

```text
Your script
   ↓ sends a prompt
Local inference runtime
   ↓ prepares the prompt
Model runs on the CPU or GPU
   ↓ produces tokens
Runtime returns the response
   ↓
Your script displays or saves it
```

A **token** is a small piece of text the model works with. The model produces its answer one token at a time. For a VLM, the request also includes an image, which the runtime prepares for the model.

## 4. Downloading, starting, and loading are different

These are separate steps:

1. **Download the model:** saves model data to the computer. For example, `ollama pull qwen3:0.6b`.
2. **Start the runtime:** starts the Ollama service so it can receive requests.
3. **Run inference:** a script sends a prompt. Ollama loads the selected model as needed and uses it to generate a response.

Downloading a model does not run it. Starting Ollama starts the service, but it does not necessarily mean a particular model is already loaded in memory. Ollama's API reports model load time and has a setting to keep a model loaded or unload it after a chosen time. [Ollama API documentation](https://docs.ollama.com/api/generate)

## 5. Ways to run inference

Different tools provide different ways to use a model:

- **Command line:** enter a prompt in a terminal program.
- **Local API:** a script sends a request to a server running on the same computer.
- **In-process library:** a Python program loads and runs the model inside that program.
- **Inference server:** a runtime runs as a service and accepts requests from one or more apps.

Our experiment used a **local API**. The Python script sent a request to Ollama at `127.0.0.1:11434`. `127.0.0.1` means “this same computer.” The API request includes a model name and prompt; the response can include generated text and timing information. [Ollama API documentation](https://docs.ollama.com/api/generate)

Other runtimes offer similar options. For example, `llama.cpp` includes an HTTP server for running models and accepting API requests. We will study that runtime in its own chapter. [llama.cpp server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

## 6. Where the model runs

The runtime performs the calculations using the available hardware:

- **CPU:** the computer's general-purpose processor. It can run inference, though it may be slower.
- **GPU:** a processor built to handle many calculations at once, often useful for model inference.
- Some runtimes can use both, depending on the computer and model.

On our Mac, Ollama handles the details of using the available hardware. We do not need to manually place model layers on a processor in our current exercises.

## 7. Why inference needs more memory than the model file

The model file is only part of the memory needed during generation. The runtime also needs room for temporary calculations and the **KV cache**. The KV cache stores information about the prompt and generated tokens so the model can use the context efficiently.

Memory use can grow with longer prompts, longer answers, and image input. Quantization can reduce the space used by model weights, as we learned in Chapter 4. Context and memory will come up again in a later chapter.

## 8. Two ways to describe speed

- **Time to first token:** how long it takes before the model starts replying.
- **Generation speed:** how quickly it produces tokens after that, often measured in tokens per second.

The first request may take longer if the runtime needs to load the model. Later requests may be faster while the model stays loaded. Ollama's API reports values such as model load time and token generation time. [Ollama API documentation](https://docs.ollama.com/api/generate)

## 9. Does local mean offline?

The model can generate responses on the computer without sending prompts to a cloud model, once the required software and model are available locally. But an app using a local model may still use the internet for other tasks, such as web search or calling an online service.

“Local inference” means the model calculations happen on the computer. It does not automatically mean every part of an app is offline.

## 10. Inference is not an agent

Inference produces a model response. By itself, it does not decide to run a script, search the web, or control a robot.

An **agent** is a larger program that can use model responses, call tools, and continue through multiple steps. We will study agents later.

## 11. Connecting this to our experiments

We downloaded a model with `ollama pull`. Ollama provides the local runtime and API service. Our Python script sends a prompt to that service, and the runtime uses the model to generate a response.

```text
ollama pull → save the model
Start Ollama → start the local service
Run the Python script → send a prompt through the API
Ollama → run the model and return the response
```

## Key takeaways

- Local inference is using a model on your own computer to produce an answer.
- A model is the learned data; the runtime is the software that runs it.
- Downloading a model, starting a runtime, and running inference are different steps.
- Our Python experiment sends its request to Ollama's local API.
- Inference uses memory for more than model weights, including the KV cache and temporary calculations.
- A local model can be part of an app that still uses internet services.
- Inference alone is not an agent; an agent adds decisions and tool use around the model.

## References

- [Ollama: Generate a response API](https://docs.ollama.com/api/generate)
- [llama.cpp: HTTP server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [Hugging Face Transformers: Pipelines](https://huggingface.co/docs/transformers/en/pipeline_tutorial)
