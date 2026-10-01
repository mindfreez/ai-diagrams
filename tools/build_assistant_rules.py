"""Builds the "Which rules each assistant reads" map in both places:
  - GitHub Pages: diagrams/assistant-rules/index.html (orb-flow template CSS, phone first)
  - Obsidian:     Shared\\Maps\\Assistant rules.canvas + .png (a 2x snapshot of the page), copied into this repo too
Edit the content lists below, run this script, then commit and push."""
import json, pathlib, re, shutil, subprocess, sys
REPO = pathlib.Path(__file__).resolve().parents[1]
DEST = REPO / "diagrams" / "assistant-rules"
CANVAS = pathlib.Path(r"C:\AI Workspace\Shared\Maps\Assistant rules.canvas")

# ---- content (shared by the page and the canvas) ----
TITLE = "Which rules each assistant reads"
INTRO = ("Claude and ChatGPT/Codex share one master rules file, and each also reads its own settings. "
         "A Codex-only rule in the workspace AGENTS.md was also being read by Claude, so Claude showed a Codex usage line. "
         "That section is now marked Codex only.")
FILES = [  # (id, name, path, lines)
    ("shared", "Shared rules", r"Shared\ASSISTANT-RULES.md", ["Master copy for both assistants", "Usage line: Claude uses get_usage, ChatGPT its own readout"]),
    ("claudemd", "Claude global", r"~\.claude\CLAUDE.md", ["Only points at the shared rules"]),
    ("codexmd", "Codex global", r"~\.codex\AGENTS.md", ["Points at the shared rules", "Codex's own working rules"]),
    ("agents", "Workspace AGENTS.md", r"C:\AI Workspace\AGENTS.md", ["Read by both when opened in that folder", "Codex usage footer: now marked Codex only"]),
]
BOTS = [
    ("claude", "Claude", "Code tab · Opus / Sonnet", ["Reads: Claude global → Shared rules", "Reads: workspace AGENTS.md", "Plus: its own memory folder", "Skips: the Codex footer section"]),
    ("codex", "ChatGPT / Codex", "Codex agent", ["Reads: Codex global → Shared rules", "Reads: workspace AGENTS.md", "Uses: the Codex footer section"]),
]
OUTS = [
    ("cl-usage", "Claude usage line", "end of each reply", ["Format: Claude 5h % · Week % · reset times", "From get_usage (also feeds the usage widget)"]),
    ("cx-usage", "Codex usage line", "end of each reply", ["Format: Codex 5h % · Week % · reset times", "From get_usage_limits"]),
    ("worklog", "Work logs", r"Shared\Worklog", ["Each assistant logs what it did", "Read the other's newest entries first"]),
]
FIXED = ("Fixed 30 Sep 2026", "Claude was following the Codex footer rule in the workspace AGENTS.md. "
         "That section now says Codex only, and Claude shows only its own usage. "
         "A cleaner option: move the Codex footer into Codex's own global file.")

# ---- page ----
ICON = {"file": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
        "bot": '<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 8V4M9 13h.01M15 13h.01M9.5 16.5h5"/><circle cx="12" cy="3.5" r="1"/>',
        "gauge": '<path d="M4 18a8 8 0 1 1 16 0"/><path d="m12 18 4-6"/>', "log": '<path d="M6 4h12v16H6z"/><path d="M9 8h6M9 12h6M9 16h4"/>'}
def node(name, sub, lines, icon, delay):
    lis = "".join(f"<li><b>{l.split(': ', 1)[0]}</b>{l.split(': ', 1)[1]}</li>" if ": " in l else f"<li>{l}</li>" for l in lines)
    return (f'<div class="node"><div class="orb" style="--delay:{delay}s"><svg viewBox="0 0 24 24">{ICON[icon]}</svg></div>'
            f'<h3>{name}</h3><div class="sub">{sub}</div><ul>{lis}</ul></div>')
tpl = (REPO / "templates" / "orb-flow.html").read_text(encoding="utf-8")
css = tpl[tpl.index("<style>"):tpl.index("</style>")] + """
.node .sub code, .sub { overflow-wrap: anywhere; }
.fixed { border: 1px solid #3ddc9755; border-radius: 18px; padding: 14px 18px; background: #3ddc970d; max-width: 70ch; margin: 0 auto; }
.fixed b { color: var(--local); font: 500 12px/1 var(--mono); letter-spacing: .14em; text-transform: uppercase; display: block; margin-bottom: 6px; }
@media (min-width: 980px) { .flow { grid-template-columns: 300px 70px minmax(0, 1fr) 70px 280px; } .orbs.local { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
"""
body = f"""<main>
  <header><h1>{TITLE}</h1><p>{INTRO}</p></header>
  <section class="flow" aria-label="Rule files, assistants and what they show">
    <div class="zone you"><h2>Rule files</h2><div class="orbs asks">
      {''.join(node(n, f'<code>{p}</code>', l, 'file', -i * 1.5) for i, (_, n, p, l) in enumerate(FILES))}
    </div></div>
    <div class="link"><span>read by</span><span class="dots"></span></div>
    <div class="zone pc"><h2>Assistants</h2><div class="orbs local">
      {''.join(node(n, s, l, 'bot', -i * 2) for i, (_, n, s, l) in enumerate(BOTS))}
    </div></div>
    <div class="link results"><span>shows</span><span class="dots"></span></div>
    <div class="zone out"><h2>What they show</h2><div class="orbs">
      {''.join(node(n, s, l, 'log' if i == 'worklog' else 'gauge', -k * 2.5) for k, (i, n, s, l) in enumerate(OUTS))}
    </div></div>
  </section>
  <p class="fixed"><b>{FIXED[0]}</b>{FIXED[1]}</p>
  <footer>Part of <a href="https://github.com/mindfreez/ai-diagrams" style="color:var(--muted)">mindfreez/ai-diagrams</a></footer>
</main>"""
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<meta name="description" content="Map of which rule files Claude and ChatGPT/Codex read, and the usage line each shows.">\n<title>Assistant rules map</title>\n'
        + re.search(r'<link rel="preconnect".*?display=swap">', tpl, re.S).group(0) + "\n" + css + "body{margin:0}</style>\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
DEST.mkdir(parents=True, exist_ok=True)
(DEST / "index.html").write_text(page, encoding="utf-8")

# ---- Obsidian: 2x desktop snapshot on a canvas (shared tool) ----
subprocess.run([sys.executable, str(REPO / "tools" / "snapshot_obsidian.py"), "assistant-rules", "Assistant rules"], check=True)
print("wrote", DEST / "index.html")
sys.exit(subprocess.run([sys.executable, str(REPO / "tools" / "check_public.py")]).returncode)
