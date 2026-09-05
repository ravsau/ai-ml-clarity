# What Is a System Prompt and Who Can See It?

## Short Answer

A **system prompt** is the block of text at the top of the context that sets the model's behavior, tone, and rules. It is ordinary input, and the model can see and even repeat it. Treat it as a suggestion to the model, not a secret.

## Where It Sits

The system prompt is the first thing in the context window, before the conversation history.

```
┌─────────────────────────────────────────────────────────────┐
│                     CONTEXT WINDOW                           │
│                                                             │
│  [System prompt]         ← the system prompt                │
│  [Prior turns...]        ← earlier user/assistant messages  │
│  [User turn]             ← the current user message         │
│                                                             │
│  ▲ Everything here = the model can see it                   │
└─────────────────────────────────────────────────────────────┘
```

## It Is Just Tokens

The system prompt is not hidden weights or special model wiring — it is plain text tokenized like any other input. There is no "memory" or "imprint" left behind. The model does not secretly memorize it any more than it secretly memorizes the rest of the context. Because it is just tokens, you can ask the model to repeat it, and it can read it back verbatim if asked.

## Not a Security Boundary

A system prompt cannot stop the model from reading the rest of the conversation, and it cannot enforce the rules it describes. Instructions in a system prompt are requests the model may follow; they are not enforcement. Anything that must be enforced — access control, secrets handling, input filtering — belongs outside the model, in the application layer.

## Related

- [what-is-context-window.md](what-is-context-window.md)
- [context-window-vs-memory.md](context-window-vs-memory.md)

## One-Liner

```
System prompt = instructions in the context window
It is ordinary input, not hidden weights
It is a request, not a security boundary
```