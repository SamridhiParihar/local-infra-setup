# Chapter 2 — LLM and VLM Model Basics

This chapter explains what a language model contains, how it generates text, and how vision and tool use fit into the picture. The examples use the local `qwen3:0.6b` model.

## 1. What a model is

A trained model is a program structure plus learned numerical values called **weights**. The structure describes the calculations. The weights hold patterns learned during training.

The model does not look up a stored answer for every question. During **inference**, it uses its weights and the current input to calculate an output. In ordinary inference, the weights do not change.

The model is part of a larger setup:

- **Architecture/configuration** describes the model's structure and settings.
- **Weights** are the learned numerical values.
- **Tokenizer** converts text to model tokens and converts generated tokens back to text.
- **Runtime**, such as Ollama, loads the model and performs the calculations.
- **Application** sends prompts and may provide tools or other context.

The downloaded model files contain more than one simple, human-readable list of weights. They can include weight data, metadata, and configuration information. The runtime uses these pieces together.

## 2. Parameters and model size

A **parameter** is one learned numerical value in the model. Parameter count gives a rough sense of model scale, but it does not by itself tell us the exact disk, memory, or speed requirements.

Our Ollama output reports:

- Model tag: `qwen3:0.6b`
- Parameter count: `751.63M` (about 752 million)
- Architecture: `qwen3`
- Quantization: `Q4_K_M`

The `0.6b` tag is a rounded size label; Ollama reports the more specific parameter count. Quantization changes how the weights are stored and represented. We will study its formats and trade-offs in a later chapter.

## 3. Text, tokens, and tokenizers

Language models process **tokens**, not words in the same way people do. A token can be a whole word, part of a word, punctuation, or a special control marker. The exact split depends on the model's tokenizer.

A **tokenizer** maps text pieces to token IDs (numbers). The model works with those IDs and internal numerical representations. When it generates token IDs, the tokenizer maps them back to readable text.

Tokenizers are made for particular model families and must match the model. Different tokenizers can assign different IDs to the same text, so using the wrong tokenizer can break the model input and output.

Many tokenizers use methods related to byte-pair encoding (BPE), but not all use the same method. A common idea is to represent frequent text pieces efficiently and split less common text into smaller pieces. The exact tokenization rules are stored with the model setup; it is not safe to assume every tokenizer uses the same greedy matching algorithm.

## 4. How text generation works

Text generation is **autoregressive**: the model predicts one next token, adds it to the sequence, then predicts another.

The simplified path is:

```text
Prompt text
  → tokenizer
  → token IDs
  → model calculations
  → scores for possible next tokens
  → choose a token
  → add it to the sequence and repeat
  → generated text
```

For each next-token step, the model produces a score called a **logit** for each possible token in its vocabulary. Larger scores mean the model currently favors those tokens more. A **softmax** calculation turns the scores into probabilities that add up to 1. Generation settings then affect how a token is selected.

This is a simplified view. Runtimes use optimized calculations and may process the initial prompt in a different way from later generated tokens.

## 5. Sampling settings

Sampling settings change how the runtime chooses from likely next tokens. They do not change the trained weights.

Ollama showed these settings for our model:

- **Temperature (`0.6`)** changes how concentrated or varied token choices are. Lower values usually make choices more predictable; higher values usually allow more variation. It is not a direct quality or safety setting.
- **Top-k (`20`)** keeps at most the 20 highest-scoring candidates for a choice.
- **Top-p (`0.95`)**, also called nucleus sampling, keeps a set of likely candidates whose combined probability reaches the configured threshold. The set can be smaller or larger depending on the current probability distribution.
- **Repeat penalty (`1`)** is neutral in this setup; values other than 1 can discourage or adjust repeated tokens, depending on the runtime's implementation.
- **Stop tokens** tell the runtime when a generated sequence or message has ended.

Temperature, top-k, and top-p can be applied together. Their exact interaction depends on the runtime. Do not assume that changing one setting always makes an answer better.

## 6. Context length and KV cache

The **context** is the tokens available to the model during one request. It can include the prompt, conversation history, tool results, and generated response, depending on how the application sends them.

Our model reports a context length of **40,960 tokens**. This is a maximum supported limit, not permanent memory. Information from a previous request is available only if the application includes it again in a later request.

During generation, the model needs to use earlier tokens to help predict the next one. In transformer models, a runtime can keep intermediate attention data for earlier tokens in a **key-value cache**, usually called the **KV cache**. Reusing this cache avoids repeating some calculations for the entire history at every generation step.

The KV cache uses memory, and its size generally grows as the context gets longer. Its exact size depends on the architecture, data type, and runtime. It is not always stored in a separate GPU memory pool: on Apple Silicon, CPU and GPU share unified memory; other systems may use discrete GPU memory.

## 7. LLMs and VLMs

- A **large language model (LLM)** takes text as its main input and generates text.
- A **vision-language model (VLM)** can use image information along with text.
- **MLLM** is another commonly used term for a multimodal large language model; multimodal models may handle images, audio, video, or other input types depending on the model.

Many VLMs use a vision encoder to turn an image into numerical features, then connect those features to a language model. The model can then use image and text information together. Designs differ: not every VLM has the same components or training method.

Images can become many visual tokens or features, so image resolution and image processing can affect context use, memory, and speed. A text-only model cannot inspect an image just because the prompt asks about it; the application must use a model that accepts image input and pass the image in the format that model expects.

Our current Qwen3 exercise is text-only. We have not yet run a VLM experiment.

## 8. Tool-use capability

A model with **tool-use capability** can produce a structured request for a tool when the application provides tool descriptions. For example, it may request a calculator with an expression.

The model does not execute the calculator. The application reads the request, runs the tool, and sends the result back to the model. Tool use often works better when the model has been trained or tuned to produce the expected request format. The exact format depends on the model and API.

Ollama reports that Qwen3 supports tools, but our experiment script sends a normal text prompt to `/api/generate`. It does not provide tools or execute tool calls. This experiment is inference, not an agent loop.

## 9. Training, fine-tuning, and inference

- **Pre-training** teaches a model broad patterns from a large training dataset by updating its weights.
- **Fine-tuning** continues training a model on a narrower dataset or task. It changes the model's behavior by updating weights or additional trainable values.
- **Inference** uses a trained model to produce outputs. The model weights are normally fixed during inference.

**LoRA** is one fine-tuning method. It keeps the original weights frozen and trains small added weight matrices. This can make adaptation cheaper than updating every original weight, but it still requires a training process. LoRA is not used by our current prompt experiment.

## 10. What we observed in `qwen3:0.6b`

`ollama show qwen3:0.6b` reported:

| Field | Reported value | Meaning |
|---|---:|---|
| Architecture | `qwen3` | Model family/architecture label |
| Parameters | `751.63M` | Approximate count of learned values |
| Context length | `40960` | Reported maximum context capacity in tokens |
| Embedding length | `1024` | A model-internal vector dimension; it is not the context length |
| Quantization | `Q4_K_M` | Quantized weight representation; detailed study is in a later chapter |
| Capabilities | completion, tools, thinking | Features Ollama identifies for this model |
| Temperature | `0.6` | Default generation setting reported by Ollama |

The script sent a text prompt to Ollama's local API. Ollama loaded the model as needed, generated a response, and returned timing and token metrics. This run did not train the model, fine-tune it, process an image, or execute a tool.

## Key takeaways

- A model predicts output from its input using learned weights; inference normally leaves those weights unchanged.
- Text is converted to model-specific tokens before the model processes it.
- Generation repeats next-token prediction until it stops.
- Sampling settings affect token selection, while context length limits how much input and history can be used in one request.
- A VLM can process image information, but model designs vary and the application must pass the image correctly.
- Tool support means the model can request tools in a format an application can handle; the application executes the tools.
- Parameter count, file size, memory use, context length, and speed are related but are not interchangeable measurements.

## Later practical exercise

Run a local VLM with an image, record the model and image details, and compare its behavior and resource use with the text-only experiment. This exercise is intentionally not completed yet.
