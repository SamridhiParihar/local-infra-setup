# Chapter 7 — `llama.cpp`

## 1. What `llama.cpp` is

`llama.cpp` is software for running language models. It is written in C and C++, and is designed to run on different kinds of computers, including Apple Silicon Macs. It supports inference on CPUs and GPUs, and can split some of the work between them. [Official `llama.cpp` project](https://github.com/ggml-org/llama.cpp)

Like Ollama, it can run a model locally. Ollama gives you a model library and a service to manage. `llama.cpp` gives you more direct control over the model file and how it runs.

## 2. How it fits with GGUF

`llama.cpp` is closely associated with **GGUF**, the model file format from Chapter 3. A GGUF file can contain model weights and information the runtime needs, such as model settings and tokenizer data.

The file is the model data. `llama.cpp` is the software that reads that data and runs inference with it. You can use a compatible model file already on your computer, or use `llama.cpp` tools to download a model from a supported source. [Official `llama.cpp` project](https://github.com/ggml-org/llama.cpp)

## 3. What happens when it runs a model

The process is similar to the local inference flow from Chapter 5:

```text
You choose a model file and send a prompt
                 ↓
llama.cpp reads the model and prepares the prompt
                 ↓
The model runs using the available CPU and/or GPU
                 ↓
llama.cpp returns the generated text
```

The model needs to fit the computer's available memory well enough to run. Quantization can make model weights smaller, though inference also uses memory for the KV cache and other calculations.

## 4. Two ways to use it

`llama.cpp` provides two common ways to run a model:

- **Command-line mode:** run a prompt directly from the terminal. This is useful for trying a model or running a small experiment.
- **Server mode:** start a local service. A script or app can send it prompts through an API, similar to how our Python script talks to Ollama.

The server also includes a web interface and API options that work with common app formats. An app can often connect to the server without running the model directly inside the app. [Server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

## 5. How it uses the hardware

`llama.cpp` has different **backends**: software parts that let it use different processors.

On an Apple Silicon Mac, it can use Apple's Metal framework to run work on the GPU. It can also run on the CPU, or use both CPU and GPU for parts of a model. This can help when a model is larger than the available GPU memory. [Official `llama.cpp` project](https://github.com/ggml-org/llama.cpp)

The exact speed depends on the model, quantization, settings, and hardware. Using a GPU does not guarantee every task will be faster.

## 6. Quantization and settings

`llama.cpp` supports models with different weight precisions, including several quantized formats. Quantization can reduce the space needed for model weights and may make a model practical to run on a smaller computer. It can also affect the model's output quality, as we learned in Chapter 4. [Official `llama.cpp` project](https://github.com/ggml-org/llama.cpp)

When launching a model, `llama.cpp` can take settings for context size, number of generated tokens, CPU threads, and how much of the model to place on a GPU. These settings give more control, but also add choices to understand and tune.

## 7. How it compares with Ollama

| Ollama | `llama.cpp` |
|---|---|
| Manages model downloads and names for you | Often works directly with a model file or a selected model download |
| Provides a background service and local API | Can run in the terminal or start its own local server |
| Hides many runtime choices behind simpler commands | Exposes more settings for how a model runs |
| Convenient for getting started with local models | Useful when you want direct control or want to study runtime behavior |

Both can run models locally and provide an API for scripts. You do not need to use both for every experiment; learning each one helps explain different ways to set up local inference.

## Key takeaways

- `llama.cpp` is an inference runtime, not a model.
- It is closely associated with GGUF model files.
- It can run models from the terminal or serve them to an app through an API.
- It supports CPU, GPU, and some CPU-plus-GPU setups.
- It gives more direct control over runtime settings than Ollama.
- Quantized weights can reduce memory needs, but inference still needs memory for other work.

## References

- [`llama.cpp` project](https://github.com/ggml-org/llama.cpp)
- [`llama.cpp` server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
