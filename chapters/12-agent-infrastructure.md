# Chapter 12 — Agent Infrastructure

## 1. What makes a program an agent?

A model can read a prompt and generate a reply. An **agent** is a larger program that uses a model to choose steps, call tools, and respond to the results.

The model is one part of the agent. Another part, the **orchestrator**, runs the process around it.

```text
User asks for a task
        ↓
Orchestrator sends the request and available tools to the model
        ↓
Model replies or requests a tool
        ↓
Orchestrator runs the tool and sends its result back
        ↓
Model replies or requests another tool
        ↓
Orchestrator stops when the task is complete
```

## 2. What happens when a model requests a tool?

Suppose a user asks for the weather. The app tells the model that a `get_weather` tool is available, what it does, and what information it needs.

The model may return a structured request such as:

```text
Tool: get_weather
City: Hyderabad
```

That is the model **requesting** the tool. It has not looked up the weather or run code itself.

The orchestrator then:

1. Checks which tool the model requested.
2. Checks the arguments, such as the city name.
3. Runs the matching function.
4. Sends the result back to the model.
5. Asks the model to use that result in its answer.

Ollama's tool-calling example follows this pattern: the model returns a tool call, the app runs the function, and the app passes the tool result back to the model. [Ollama tool-calling guide](https://docs.ollama.com/capabilities/tool-calling)

## 3. Main parts of an agent system

- **Model:** interprets the request and suggests a response or tool call.
- **Orchestrator:** sends messages, runs the loop, and decides when to stop.
- **Tools:** functions the app makes available, such as reading a file or calling an API.
- **State:** information the app keeps during the task, such as previous messages and tool results.
- **Data sources:** places a tool can read from, such as documents or databases.

A model can be trained to produce tool-call formats, but the app must still provide the real tools and execute them.

## 4. Conversation context and memory

An agent often needs to keep track of what has already happened:

- **Conversation context** is the messages and tool results sent to the model for the current task. It helps the model continue from the previous step.
- **Long-term memory** is information saved outside that conversation, such as in files or a database, that can be retrieved in a later task.

The model does not automatically remember every past interaction. The app must decide what to store and what to send back as context.

## 5. Agent, MCP client, and MCP server

**MCP**, or Model Context Protocol, is a standard way for AI apps to connect to tools and data sources. Think of it as a shared connector standard. MCP does not provide the model or make an app an agent by itself. The app still coordinates the model and decides how to handle tool requests. [MCP introduction](https://modelcontextprotocol.io/introduction)

Example: you ask, “Find the model-format notes in my project and summarize them.”

```text
Agent (model + coordinator)
    ↕
MCP client (connector inside the app)
    ↕
MCP server (provides a search-files tool)
```

1. The MCP server tells the MCP client that it can search project files.
2. The agent gives that tool information to the model.
3. The model requests a file search.
4. The agent asks its MCP client to send that request to the server.
5. The server searches the files and returns results through the client.
6. The agent gives the results to the model, which writes the summary.

The **agent decides what to ask for and coordinates the task**. The **MCP client carries messages**. The **MCP server provides and runs the search tool**.

## 6. Give tools clear limits

Tools give an agent the ability to affect other systems, so the orchestrator should limit what tools can do. For example, it can allow a model to read a folder but require confirmation before deleting a file.

The model's tool request is a suggestion from generated output. The app should check that the tool and its arguments are allowed before executing it. MCP's specification calls out user control, consent, and protection of data and operations. [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25)

## 7. How this connects to robotics

For a robot, tools could provide sensor readings, request a map, or ask a motion system to perform an action.

A sensible design gives the model a **high-level role**, such as deciding which task to attempt. A separate controller handles precise movement and checks that actions remain within safe limits. The model should not be the only layer deciding whether motors can move.

## 8. Where we are in our project

Our current Python experiment sends a prompt to Ollama and records the response. That is local inference, but it is not yet an agent loop because the script does not give the model tools and then execute its tool requests.

To make it an agent, we would add:

1. One or more tool definitions.
2. Code that maps each tool name to a real function.
3. A loop that sends tool results back to the model.
4. A clear stopping rule.

## Key takeaways

- An agent is a model plus an orchestrator, tools, and state.
- A tool call is the model asking the app to run a function; the model does not run the function itself.
- The orchestrator checks and executes the request, then returns the result to the model.
- An MCP client connects the agent app to MCP servers; MCP servers provide tools or data.
- An agent can use tools without MCP, and MCP alone does not make an app an agent.
- Tool access should be limited to what the task needs.
- In robotics, use the model for high-level decisions and a separate controller for precise actions and safety checks.

## References

- [Ollama tool-calling guide](https://docs.ollama.com/capabilities/tool-calling)
- [MCP introduction](https://modelcontextprotocol.io/introduction)
- [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25)
