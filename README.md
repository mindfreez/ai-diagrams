# AI diagrams

Visual maps of a two-PC home AI setup: local models, assistants, and how data flows between them.
Live pages: **https://mindfreez.github.io/ai-diagrams/**

| Diagram | Page | Obsidian |
|---|---|---|
| Local AI at a glance | [diagrams/local-ai-overview](https://mindfreez.github.io/ai-diagrams/diagrams/local-ai-overview/) | `diagrams/local-ai-overview/overview.canvas` |
| Which rules each assistant reads | [diagrams/assistant-rules](https://mindfreez.github.io/ai-diagrams/diagrams/assistant-rules/) | `diagrams/assistant-rules/assistant-rules.canvas` |

## This repo is public
- **Only public-safe content.** No chats or chat history, personal or client details, addresses, account names beyond the GitHub username, keys/tokens, or private file contents.
- Anything with private or personal info goes in the separate **private** repo `mindfreez/ai-diagrams-private`.
- Before every commit, run `python tools/check_public.py`. It refuses obvious secrets and private markers.

## Layout
- `diagrams/<name>/index.html`: the animated page (also published on GitHub Pages).
- `diagrams/<name>/*.canvas`, `*.svg`: Obsidian versions. Open this repo folder as an Obsidian vault ("Obsidian Diagrams").
- `tools/`: scripts that build the diagrams and run the public check.
