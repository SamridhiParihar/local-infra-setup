# Chapter 11 — Benchmarking

## 1. What benchmarking means

A **benchmark** is a planned, repeatable way to measure how a model performs on a particular computer and task.

One model run gives an example result. A benchmark runs consistent prompts and records measurements so you can compare, for example, two models or two runtimes.

There is no single number that describes a model's performance. A model can generate quickly but give poor answers, or produce good answers while taking longer.

## 2. What to measure

### Speed

- **Model load time:** how long the runtime takes to load the model.
- **Time to first output:** how long until the model begins replying. A common server metric is **time to first token (TTFT)**.
- **Generation speed:** how quickly it produces tokens, often measured in **tokens per second**.
- **Total response time:** how long the whole request takes.

These measure different things. A quick first token does not guarantee that the full answer will finish quickly.

### Memory and hardware use

You may also measure peak memory, GPU use, and whether the computer starts using swap. These help show how much work the model puts on your machine.

Ollama's API reports timings and counts such as model load time, prompt evaluation time, output token count, and generation time. It does not report your Mac's full memory use, so that needs a separate monitor, such as Activity Monitor. [Ollama API response fields](https://docs.ollama.com/api/generate)

### Answer quality

Speed is only useful if the answer is good enough for the task. Use the same questions for each model and compare the results against a simple checklist. For example: “Did it answer all parts? Was it correct? Did it follow the requested format?”

## 3. One user versus many users

For a single prompt, you might care most about how soon the answer starts and how long it takes to finish.

For a server handling many requests, measure **throughput** too: the total work it completes over time. Also track latency at different loads. For example, **p95 latency** means 95% of requests finished within that time; it shows how slower requests behave, not just the average.

Serving systems such as vLLM expose metrics for first-token time, time between tokens, total request latency, and number of waiting requests. [vLLM production metrics](https://docs.vllm.ai/en/latest/usage/metrics/)

## 4. Make comparisons fair

When comparing two runs, keep the important conditions the same:

- Same computer and background workload
- Same model and model version or quantization
- Same prompt and input data
- Same generation settings and answer length limit
- Same runtime version, when comparing runtimes

Also separate **cold runs** from **warm runs**. A cold run includes loading the model; a warm run starts with the model already loaded. Mixing them can make the comparison confusing.

Run each setup more than once. Use the median—the middle result after sorting the runs—to reduce the effect of one unusually slow run.

## 5. How to read our earlier Ollama result

Our earlier script run reported:

- Model load time: about **1.56 seconds**
- First output chunk: about **4.09 seconds**
- Generation speed: about **102.7 tokens per second**

Those measurements describe different parts of the run. The “first output chunk” is the time our script observed its first returned text chunk. Treat it as the script's measurement, rather than assuming it is identical to a standardized server metric such as TTFT.

The script also noted that memory and GPU use needed a separate sampler. So the result tells us about timing and token output, but it does not tell us how much RAM or GPU memory the model used.

## 6. A simple benchmark plan

For a basic local-model comparison:

1. Choose one model and one prompt.
2. Decide on a fixed maximum answer length and generation settings.
3. Run once to warm up the model.
4. Run several measured requests under the same conditions.
5. Record load time, first output time, output tokens, generation speed, and memory pressure.
6. Repeat with the next model or runtime.
7. Compare speed **and** answer quality.

Later, when we benchmark a server, we can add multiple simultaneous requests and measure throughput and p95 latency.

## Key takeaways

- Benchmarking is a repeatable comparison, not just one model run.
- Load time, first output, generation speed, total response time, memory use, and quality measure different things.
- Keep model, prompt, settings, and computer conditions consistent.
- Measure cold and warm runs separately, and repeat runs.
- Our earlier experiment measured timing and tokens; it did not measure RAM or GPU use.

## References

- [Ollama API response fields](https://docs.ollama.com/api/generate)
- [vLLM production metrics](https://docs.vllm.ai/en/latest/usage/metrics/)
