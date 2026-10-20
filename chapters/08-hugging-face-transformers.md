# Chapter 8 — Hugging Face Transformers

## 1. Two meanings of “transformer”

A **Transformer** is a type of neural network architecture used inside many language models.

**Hugging Face Transformers** is a Python library that helps you load and use models built with architectures such as Transformers. It supports inference and training, and works with text, images, audio, video, and multimodal models. [Transformers documentation](https://huggingface.co/docs/transformers/index)

## 2. What the library gives you

A model needs more than its weights. Your program also needs to know how to prepare the input and run the correct model design.

Transformers provides pieces for this, including:

- **Model:** the code and weights that perform the model's calculations.
- **Tokenizer or processor:** prepares the input. A tokenizer handles text; a processor may handle images, audio, or multiple input types.
- **Configuration:** describes details such as the model architecture and its settings.

These pieces need to match the model checkpoint—the saved model weights. Transformers can load weights and configuration from the Hugging Face Hub or from local files. [Loading models](https://huggingface.co/docs/transformers/en/models)

## 3. The request flow

When your Python program uses a model through Transformers, the flow looks like this:

```text
Python program
   ↓ sends text or other input
Tokenizer or processor prepares it
   ↓ turns it into model-ready data
Model runs on CPU or accelerator
   ↓ produces output
Tokenizer or processor turns output into readable form
   ↓
Python program receives the result
```

For text, the tokenizer converts the prompt into token IDs. The model processes those IDs and generates output tokens. The tokenizer converts them back into text. For images and other inputs, the matching processor prepares that data for the model.

## 4. Two ways to use it

Transformers has a convenient, high-level option called **`pipeline`**. You choose a task, such as text generation, and give it a model and input. The pipeline handles much of the preparation and output conversion for you. Pipelines also support tasks such as image classification and speech recognition. [Pipeline tutorial](https://huggingface.co/docs/transformers/en/pipeline_tutorial)

You can also load the model and tokenizer separately. This gives you more control over each step, such as how the prompt is prepared, where the model runs, or how generation is configured.

- **Pipeline:** less setup; useful for trying a task.
- **Separate model and tokenizer:** more control; useful when building a custom app or experiment.

## 5. Where the model runs

Transformers runs as part of your Python program. This differs from our Ollama setup, where the Python script sends a request to a separate local service.

Transformers can use the CPU or an available accelerator. Its pipeline guide documents support for Apple Silicon, GPUs, and CPUs. The exact hardware support and speed depend on the model, libraries, and setup. [Pipeline tutorial](https://huggingface.co/docs/transformers/en/pipeline_tutorial)

## 6. Downloading and running a model

A Transformers program can load a model from the Hugging Face Hub. The first time, this usually means downloading model files and configuration. Those files can then be loaded from the local cache or a local folder.

The model and your Python program remain separate things: the program uses the model files to perform inference. Loading a model does not train it or change its learned weights.

## 7. How it compares with Ollama and `llama.cpp`

| Tool | How your program uses it |
|---|---|
| **Ollama** | Your program sends a request to Ollama's local API service. |
| **`llama.cpp`** | Your program can use its command-line tools or send a request to its server. |
| **Transformers** | Your Python program loads the model and runs it within the program. |

They can all be used for inference, but they offer different ways to load models and connect them to applications.

Transformers is useful for learning how Python code works directly with models, tokenizers, and processors. Ollama is convenient when you want a separate local service. `llama.cpp` gives direct control over a runtime designed for efficient local inference.

## 8. Important limits

Transformers does not make every model fit on every computer. Large models can need a lot of memory. You still need compatible model files, enough available memory, and a setup that can use your computer's hardware.

Transformers supports options for choosing devices, placing a model across devices, and using some quantized models. These options can reduce memory needs or change performance, but the result depends on the model and hardware. [Pipeline tutorial](https://huggingface.co/docs/transformers/en/pipeline_tutorial)

## Key takeaways

- A **Transformer** is a model architecture; **Hugging Face Transformers** is a Python library.
- The library loads the model and the tokenizer or processor it needs.
- `pipeline` is the simpler way to try a supported task.
- Loading the model and tokenizer separately gives more control.
- Transformers runs inside your Python program; Ollama and `llama.cpp` can run as separate services.
- Your computer still needs enough memory and compatible hardware to run the chosen model.

## References

- [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers/index)
- [Loading models](https://huggingface.co/docs/transformers/en/models)
- [Pipeline tutorial](https://huggingface.co/docs/transformers/en/pipeline_tutorial)
