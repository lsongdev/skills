---
name: miya-desktop
description: Configure and troubleshoot Miya Desktop, its providers, profiles, agents, MCP servers, skills, channels, workspace, and local runtime files.
---

# Miya Desktop

Use this skill when the user asks how Miya Desktop is configured, wants a settings change, or needs help locating its local runtime files.

## Runtime Layout

- `~/.miya/config.json`: shared Miya configuration.
- `~/.miya/workspace`: default workspace and its `AGENTS.md` instructions.
- `~/.miya/skills`: user-installed skills. Each directory contains a `SKILL.md` and optional supporting files.
- `~/.miya/sessions`: persisted sessions.
- `~/.miya/cache/conversations`: Desktop conversation snapshots used for fast session display.
- `~/.miya/logs`: runtime logs.

## Configuration Model

- `providers` contains named API connections. A provider type must be supported by Miya, currently `openai` or `anthropic`.
- `profiles` are built-in agents. A profile references a provider and model and may define its workspace and token limits.
- `agents` contains only external ACP endpoints. Built-in agents are derived from profiles and must not be duplicated here.
- `mcpServers` contains stdio, streamable HTTP, HTTP, or SSE MCP connections.
- `channels` contains remote channel instances and their agent bindings.

When renaming a provider, update every profile that references the old provider name. When changing agent, provider, profile, MCP, or channel configuration, explain that reconnecting or restarting the relevant service may be necessary.

## Safety

1. Read the existing JSON before changing it.
2. Preserve unknown and unrelated fields.
3. Never invent or reveal API keys, tokens, passwords, or authorization headers.
4. Keep valid JSON with two-space indentation.
5. Prefer the Desktop Settings UI for ordinary changes. Edit the file directly only when the UI cannot express the requested configuration.
6. Do not delete session, cache, workspace, or log data unless the user explicitly asks.
