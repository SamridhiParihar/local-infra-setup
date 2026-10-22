# Chapter 10 — Hardware and Memory

## 1. What parts of the computer matter?

Running a model depends on several parts working together:

- **CPU:** handles general calculations and runs the operating system and apps.
- **GPU:** handles many calculations in parallel, which can speed up model inference.
- **Memory (RAM):** holds the model and the information it needs while running.
- **Storage (SSD):** keeps model files when they are not loaded for inference.

A model file being small enough to fit on the SSD does not mean it will run comfortably. The computer also needs enough memory for the model and its work.

## 2. RAM and VRAM

On many computers, the CPU uses **RAM**, while a separate graphics card has its own **VRAM**. A model running on that graphics card needs enough VRAM for the weights and other data.

The Apple M1 Pro uses **unified memory**: the CPU and GPU share the same physical memory pool. So the GPU does not have a separate pool of VRAM to add on top of the Mac's RAM. Apple describes the M1 Pro as having unified memory accessible within the chip. [Apple's M1 Pro overview](https://www.apple.com/newsroom/2021/10/introducing-m1-pro-and-m1-max-the-most-powerful-chips-apple-has-ever-built/)

The amount installed in a specific Mac is shown in **Apple menu → About This Mac**. M1 Pro models were sold with different memory configurations, so check your own Mac rather than assume a number.

## 3. How a model uses memory

While generating an answer, the computer needs memory for more than the model weights:

1. **Model weights:** the learned values stored in the model file.
2. **KV cache:** information about the prompt and generated tokens, kept so the model can use its context efficiently.
3. **Temporary working space:** memory needed for calculations and intermediate results.
4. **Other apps and macOS:** they also use system memory.

A rough estimate for weight storage is:

```text
number of parameters × bytes per weight
```

For example, storing 1 billion weights at about 4 bits each would take roughly half a gigabyte for the weights alone. The actual model package and total memory use will be higher because of extra model data, the KV cache, and runtime needs.

## 4. Why context length affects memory

The model's **context** is the text and other input it can use while answering. A longer prompt, longer conversation, or longer generated answer generally means more information must be kept in the KV cache.

This is why a model may start successfully with a short prompt but use more memory when given a much longer one. VLMs can also need extra memory to process images.

## 5. Capacity and bandwidth

Two different memory properties matter:

- **Capacity** is how much data memory can hold.
- **Bandwidth** is how quickly data can move between memory and processors.

A model may fit in memory but still run slowly if the computer cannot move the data fast enough. Apple lists the M1 Pro's unified memory bandwidth separately from its maximum memory capacity because these describe different things. [Apple's M1 Pro overview](https://www.apple.com/newsroom/2021/10/introducing-m1-pro-and-m1-max-the-most-powerful-chips-apple-has-ever-built/)

## 6. Why quantization helps—and what it does not solve

Quantization stores model weights with fewer bits, which can reduce their size in storage and memory. That may let a model fit on a computer that could not run a larger, higher-precision version.

But quantization does not remove memory needed for the KV cache, temporary calculations, or other running apps. A smaller model package does not tell us exactly how much memory inference will use.

## 7. What happens when UTM is running

A virtual machine such as UTM uses part of the Mac's physical memory for its guest operating system and apps.

The RAM assigned to a virtual machine is **not additional memory**. It comes from the Mac's existing physical memory. While the VM is running, its memory use leaves less available for macOS and other apps. When the VM is shut down, the memory it was using becomes available to the Mac again. The Mac's installed memory capacity does not change.

## 8. Checking memory on your Mac

In **Activity Monitor → Memory**, you can check:

- **Physical Memory:** how much RAM is installed.
- **Memory Pressure:** how well memory is keeping up with the work.
- **Compressed:** memory macOS compressed to make room.
- **Swap Used:** how much SSD space macOS is using as extra working space.

Apple says memory pressure reflects factors such as free memory, swap, wired memory, and cached files. A green graph generally means memory is being handled efficiently; yellow or red can indicate increasing pressure. [Apple's Activity Monitor guide](https://support.apple.com/en-ie/guide/activity-monitor/actmntr1004/10.14/mac/15.0), [Check memory pressure](https://support.apple.com/en-asia/guide/activity-monitor/actmntr34865/10.14/mac/15.0)

## Key takeaways

- The model file lives on storage; inference needs memory to use it.
- Inference memory includes weights, KV cache, temporary calculations, and other apps.
- More context usually means more KV-cache memory.
- The M1 Pro's CPU and GPU share unified memory; it does not have a separate VRAM pool.
- UTM uses a portion of the Mac's physical memory; it does not add memory.
- In Activity Monitor, check memory pressure and swap, not only the amount of memory currently used.
- Model size, memory capacity, and memory speed are related but different.

## References

- [Apple's M1 Pro overview](https://www.apple.com/newsroom/2021/10/introducing-m1-pro-and-m1-max-the-most-powerful-chips-apple-has-ever-built/)
- [Apple Activity Monitor: View memory usage](https://support.apple.com/en-ie/guide/activity-monitor/actmntr1004/10.14/mac/15.0)
- [Apple Activity Monitor: Check memory pressure](https://support.apple.com/en-asia/guide/activity-monitor/actmntr34865/10.14/mac/15.0)
