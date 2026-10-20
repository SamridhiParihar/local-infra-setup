# Chapter 9 — vLLM

## 1. What vLLM is

vLLM is software for running models and serving them to apps. It is designed to handle many requests efficiently, such as when several people or programs use the same model server. [vLLM documentation](https://docs.vllm.ai/en/latest/)

Think of it this way:

- **Ollama** makes it simple to download and run models locally.
- **`llama.cpp`** gives direct control over running a model, often from a GGUF file.
- **Transformers** lets a Python program load a model and run it itself.
- **vLLM** focuses on serving model requests efficiently, especially when requests arrive together.

## 2. Why serving many requests takes planning

When a model generates text, it keeps information about each request's context in memory. This is called the **KV cache**. If many people send long prompts, their KV caches can use a lot of GPU memory.

A server also has to decide how to share its computing time between requests. Handling each request separately can leave the GPU underused or make people wait.

vLLM is designed to manage requests and their memory efficiently.

## 3. PagedAttention: organizing the KV cache

vLLM uses a technique called **PagedAttention** to manage KV-cache memory. In simple terms, it stores the cache in smaller blocks instead of requiring one large, continuous memory area for each request.

This is similar to how an operating system manages memory in pages: data can be organized in available blocks, which helps reduce wasted space and makes it easier to serve multiple requests. [vLLM documentation](https://docs.vllm.ai/en/latest/)

## 4. Continuous batching: grouping requests as they arrive

**Batching** means running work for multiple requests together.

With **continuous batching**, vLLM can add new requests to the work as others finish, instead of waiting for every request in a group to finish before starting another group. This can help keep the GPU busy and improve the total number of tokens the server produces over time.

This is most useful when a server has many requests. It does not mean every person's answer will always start sooner; that also depends on the load, model, and hardware.

## 5. How a vLLM server works

A common setup is:

```text
App or script
      ↓ sends request
vLLM server
      ↓ schedules requests and runs the model
GPU or other supported hardware
      ↓ generates tokens
vLLM server returns the answer
```

The server provides an API for applications. vLLM supports an OpenAI-compatible API, so apps written for that API can often connect to vLLM by changing the server address. [vLLM documentation](https://docs.vllm.ai/en/latest/)

## 6. Throughput and latency

Two measurements help describe a model server:

- **Latency:** how long one request takes, including how long before the first token arrives.
- **Throughput:** how much work the server completes over time, such as total tokens generated per second across requests.

vLLM focuses on serving throughput. Its advantage becomes more relevant when a server handles multiple users or many requests, rather than one prompt at a time.

## 7. Models and hardware

vLLM supports many model architectures and has features for serving models on different hardware. Its standard installation is aimed mainly at Linux systems. The current documentation also describes **vLLM-Metal**, a separate community-maintained package for Apple Silicon that uses MLX for GPU acceleration. This path uses models optimized for MLX, so it is a different setup from the standard Linux installation. [vLLM hardware and installation guide](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/)

For our MacBook, we should distinguish learning how vLLM works from choosing how to run it. The standard vLLM setup is generally used on Linux systems; Apple Silicon support is through the separate vLLM-Metal path. We can choose the practical setup when we reach the exercise.

## Key takeaways

- vLLM is an inference and serving system, with a focus on handling requests efficiently.
- **PagedAttention** helps manage KV-cache memory in blocks.
- **Continuous batching** adds and removes requests as the server works.
- **Throughput** measures total work over time; **latency** measures the time for a request.
- vLLM is most useful when serving multiple requests, often on GPU-based systems.
- Apple Silicon support exists through the separate vLLM-Metal package, which uses MLX-optimized models.

## References

- [vLLM documentation](https://docs.vllm.ai/en/latest/)
- [vLLM hardware and installation guide](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/)
