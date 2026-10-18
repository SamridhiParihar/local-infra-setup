# Chapter 6 — Ollama

## 1. What Ollama does

Ollama is software for downloading and running models on your computer. It manages model files, starts a local service, and gives apps and scripts a way to send prompts to models.

Ollama can be used from terminal commands or through its local API. It also supports cloud models, but our exercises so far use downloaded models and run inference locally. [Ollama documentation](https://docs.ollama.com/)

## 2. The main parts

Think of Ollama as four connected parts:

- **Command line:** commands such as `ollama pull` and `ollama run`.
- **Background service:** receives requests and manages model runs.
- **Model store:** holds the model data Ollama downloaded.
- **Inference runtime:** loads the selected model and runs it using the computer's hardware.

The model is separate from Ollama. Ollama provides the software around the model so you can download it, run it, and use it from a script.

## 3. Commands we have used

- `ollama pull qwen3:0.6b` downloads that model. It does not ask the model to answer a prompt.
- `open -a Ollama` opens the Ollama app, which can start the background service. It does not open a model chat by itself.
- `ollama run qwen3:0.6b` starts using that model from the terminal. It can open an interactive prompt.
- Running `ollama` by itself may show Ollama's menu, depending on the installed version.
- Our Python script sends a request to Ollama's local API, so it can run inference without an interactive chat.

The local API is available at `http://localhost:11434/api`. Ollama also documents an OpenAI-compatible API address at `http://localhost:11434/v1`. [Ollama API introduction](https://docs.ollama.com/api/introduction)

## 4. How our script reaches the model

```text
Python script
   ↓ sends prompt and model name
Ollama API at localhost:11434
   ↓ finds and loads the selected model
Model runs on the Mac
   ↓ returns generated text
Python script displays and records the result
```

The API request tells Ollama which model to use and what prompt to send. Ollama returns the answer and can also return information such as model load time and generation time. [Ollama generate API](https://docs.ollama.com/api/generate)

## 5. Model names and tags

A model name often has a **tag**, such as `qwen3:0.6b`. A tag identifies a particular version or size of the model. A different tag may refer to another size or variant.

These commands show different things:

- `ollama list` shows models saved locally.
- `ollama show qwen3:0.6b` gives information about a model.
- `ollama ps` shows models currently loaded in memory and how Ollama is using available processors. [Ollama FAQ](https://docs.ollama.com/faq)

This helps distinguish a model **saved on disk** from one **currently loaded for inference**.

## 6. What a Modelfile does

A **Modelfile** is a set of instructions for creating a customized Ollama model entry from an existing model or supported model files.

It can set things such as:

- The base model (`FROM`)
- A system message (`SYSTEM`)
- Generation settings (`PARAMETER`)
- The prompt structure sent to the model (`TEMPLATE`)

For example, you could create a version of a model that is set up to answer in a certain style. This configures how the model is used; it does not train the original model or change its learned weights. [Ollama Modelfile reference](https://docs.ollama.com/modelfile)

## 7. Tool capability and tools

A model may be able to produce a **tool call**: a structured request to use a tool. A model's capability does not mean that it can directly control the computer.

The app or script must provide the available tools, receive the model's request, run the chosen tool, and send the result back to the model. The app carries out this loop.

## 8. Network and local use

Ollama's local service listens on `127.0.0.1` by default. This address means requests are intended for the same computer. Local API requests do not need an API key. Ollama can also be configured to expose its service on a network; that is a separate setup choice. [Ollama API introduction](https://docs.ollama.com/api/introduction), [Ollama FAQ](https://docs.ollama.com/faq)

When using a downloaded local model, Ollama says prompts and answers are not sent back to Ollama. Cloud models are different: those requests go to the hosted service. [Ollama FAQ](https://docs.ollama.com/faq)

## Key takeaways

- Ollama manages local models and provides a way to run them.
- `pull` downloads a model; `run` uses one; `open -a Ollama` opens the app and service.
- Our Python script uses Ollama's local API to request inference.
- `ollama list` shows what is stored; `ollama ps` shows what is currently loaded.
- A Modelfile configures a model entry; it does not train the model.
- A model can request a tool, but the app must provide and run that tool.

## References

- [Ollama documentation](https://docs.ollama.com/)
- [Ollama API introduction](https://docs.ollama.com/api/introduction)
- [Ollama generate API](https://docs.ollama.com/api/generate)
- [Ollama Modelfile reference](https://docs.ollama.com/modelfile)
- [Ollama FAQ](https://docs.ollama.com/faq)
