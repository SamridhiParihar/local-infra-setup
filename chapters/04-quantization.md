# Chapter 4 — Quantization

Quantization stores model weights using fewer bits. This can reduce model file size and the memory needed for weights during inference. The trade-off is that the stored numbers are less precise.

## 1. Precision and storage

A model weight is a number. Its **precision** describes how finely that number can be represented. Common formats include:

| Format | Bits per value | Rough storage per value |
|---|---:|---:|
| FP32 | 32 | 4 bytes |
| FP16 or BF16 | 16 | 2 bytes |
| INT8 | 8 | 1 byte |
| 4-bit | 4 | Half a byte |

These are simple estimates for weight values. A real model file also needs scales, metadata, and other information, so its size is larger.

## 2. How quantization works

Quantization maps original numbers to a smaller set of codes. A 4-bit code has `2^4 = 16` possible values. The original weights are approximated using those codes and a **scale**.

A simplified example is:

```text
quantized value = round(original value / scale)
estimated original value = quantized value × scale
```

The estimate may differ from the original. This difference is called **quantization error**. A scale may be shared by a group, or **block**, of weights. Some methods also use a **zero point** to represent zero accurately.

## 3. Why quantize?

The main benefit is that weights use less disk space and memory. As a rough example, 7 billion raw weight values would need about:

- 28 GB at FP32
- 14 GB at FP16 or BF16
- 7 GB at INT8
- 3.5 GB at 4-bit

These estimates cover weight values only. They do not include the KV cache, temporary calculations, runtime overhead, or other model components. Actual model files and total memory use will be higher.

Quantization can also improve speed when the hardware and runtime support efficient operations for that format. It does not guarantee faster generation on every computer.

## 4. The trade-off

Quantization reduces precision, so it can change output quality. The effect depends on the model, task, quantization method, and precision level.

A smaller file is not automatically better. A low-precision model may fit in memory but make more mistakes on tasks that need fine detail. A higher-precision model may give better results but need more memory.

To compare quantizations, run the same model and prompts at two or more levels, then compare:

- Whether each model fits in memory
- Response quality on the chosen task
- Model load time
- Generation speed
- Memory use

## 5. Common quantization approaches

**Post-training quantization (PTQ)** is applied after the model has been trained. It does not require training the full model again. Some PTQ methods use sample data, called **calibration data**, to help choose how values should be represented.

**Quantization-aware training (QAT)** accounts for quantization during training. The model is trained to handle the precision loss, so it requires a training process.

**GPTQ** and **AWQ** are names associated with quantization methods and the model checkpoints produced with them. They are not the same kind of label as FP16 or a general file container such as GGUF.

## 6. Reading a label such as `Q4_K_M`

Ollama reported `Q4_K_M` for our Qwen models. This is a quantization label used in the GGUF/`llama.cpp` ecosystem.

The `Q4` part points to a quantization family that uses roughly 4-bit weights. But the whole model does not necessarily use exactly 4 bits for every value. Some formats use blocks, scales, and mixed precision for different tensors. In the `llama.cpp` examples, `Q4_K_M` averages more than 4 bits per weight.

This is why a model's size will not exactly equal:

```text
parameter count × 4 bits
```

The model may include extra information and tensors stored at other precisions.

## 7. What quantization changes—and what it does not

Quantization changes how weights are represented. By itself, it does not:

- Change the model architecture
- Reduce the number of parameters
- Shorten the model's context length
- Train the model on new information
- Remove selected parameters

Removing selected parameters is a different technique called **pruning**. Quantization stores weights more compactly; pruning removes some of them.

Quantization also does not remove all inference memory use. The runtime still needs memory for the KV cache, temporary calculations, and other data. A VLM also has vision components that use storage and processing resources.

## 8. Connecting this to our models

Ollama reported `Q4_K_M` for `qwen3:0.6b` and `qwen3-vl:2b`. Their downloads were about 522 MB and 1.9 GB. These sizes cover the model packages and their stored tensors; parameter count multiplied by four bits is only a rough estimate for some weights.

To measure quantization's real effect, we would need versions of the same model at different quantization levels and compare them on the same computer and prompts.

## Key takeaways

- Quantization stores weights with fewer bits, usually reducing their storage and memory use.
- Lower precision introduces some error and can affect output quality.
- Smaller quantized files are not guaranteed to generate text faster.
- `Q4_K_M` is an approximate label; it does not mean every value is exactly 4 bits.
- Runtime memory includes more than model weights.
- Quantization is different from file format, training, and pruning.

## References

- [Hugging Face: Bitsandbytes quantization](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)
- [Hugging Face: AWQ quantization](https://huggingface.co/docs/transformers/quantization/awq)
- [Hugging Face: Choosing a quantization method](https://huggingface.co/docs/transformers/quantization/selecting)
- [llama.cpp quantization options](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/quantize.cpp)
- [llama.cpp quantization guide](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md)
