# Chapter 3 — Model Formats

This chapter explains how model data is saved on disk, what common file names mean, and why the inference runtime must support the model files.

## 1. Three different things

Keep these terms separate:

- **Model weights** are the learned numbers the model uses.
- **File format** describes how model data is arranged and saved on disk.
- **Quantization** describes how precisely the weight numbers are stored. Our Qwen models report `Q4_K_M`; we will study what that means in Chapter 4.

A model file can use a particular format and also store quantized weights. **GGUF** and **Q4_K_M** describe different things.

## 2. GGUF

**GGUF** is a model file format used by `llama.cpp` and compatible software. It can store model tensors—the model's numerical data—along with information needed to load the model. It is often distributed as one file, though large models can be split into parts.

Ollama can use GGUF models. However, seeing `Q4_K_M` in `ollama show` tells us about the weights' quantization; it does not by itself show the filename or prove what container format Ollama stored internally.

## 3. Safetensors

**Safetensors** is another way to save model tensors. It is common in the Hugging Face ecosystem and is designed to load tensor data without using Python's pickle format.

A Safetensors file usually holds weight data. It usually needs other model files alongside it, such as:

- `config.json` — describes the model architecture and dimensions.
- `tokenizer.json` and `tokenizer_config.json` — help convert text to tokens and back.
- `generation_config.json` — may contain settings used during text generation.
- Processor files — may describe image or other input processing for a VLM.

Larger weight sets may be split across several Safetensors files. An index file shows which weights are in each part.

## 4. PyTorch checkpoint files

You may also see files ending in `.bin`, `.pt`, `.pth`, or `.ckpt`. These names are used for saved PyTorch data, but the extensions alone do not tell you exactly what is inside. A checkpoint might hold model weights, training state, or other data.

Some older PyTorch checkpoint files use Python's pickle format. Only load these from sources you trust. Safetensors was created as a safer way to save tensor data.

## 5. Quantization names

Names such as **GPTQ** and **AWQ** are associated with ways of quantizing models and the resulting quantized checkpoints. They are not simply interchangeable with file-container names such as GGUF or Safetensors.

A quantized model may be stored in a checkpoint that also uses a particular file format. In Chapter 4, we will study how quantization changes weight storage and what its quality and memory trade-offs are.

## 6. Conversion and compatibility

The model's files need to be in a format the inference software can load:

- `llama.cpp` requires GGUF model files.
- Hugging Face Transformers commonly loads model folders containing configuration, tokenizer, and weight files.
- Ollama supports particular model families and formats. Exact compatibility depends on the model and Ollama version.

A model cannot always be loaded just because its files exist on the computer. The runtime must understand the model architecture and file format. For a VLM, the runtime must also support its image-processing parts.

**Conversion** changes how model data is arranged so another runtime can use it. It does not necessarily change the learned values. **Quantization** changes how the weight values are represented. A workflow may convert and quantize a model, but those are separate operations.

## 7. How this connects to Ollama

Your Ollama model files are stored under `~/.ollama/models`. Their names may not end in `.gguf` or `.safetensors`; Ollama stores content in its own model-store layout, so a filename alone may not reveal the underlying format.

Keep these labels separate:

- `qwen3-vl` is the model family and architecture label.
- `Q4_K_M` is the reported quantization.
- Ollama is the runtime managing the model.
- A file format describes how model data is stored.

## Key takeaways

- A model download is often a set of related files, not just one weight file.
- The runtime must support the model architecture and file format.
- Tokenizer, configuration, and processor files may be needed along with weights.
- GGUF, Safetensors, and quantization labels answer different questions about the model files.
- File conversion and weight quantization are separate operations.

## References

- [GGUF format](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
- [llama.cpp model documentation](https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md)
- [Safetensors documentation](https://huggingface.co/docs/safetensors/index)
- [Hugging Face model files](https://huggingface.co/docs/hub/en/transformers)
