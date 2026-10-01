"""Keeps every copy of the "Local AI at a glance" diagram in step. Run after editing either source:
  - page source:     C:\\AI Workspace\\Shared\\Maps\\local-ai-overview.html   (artifact-style body, no <html> wrapper)
  - Obsidian source: C:\\AI Workspace\\Claude\\tools\\build_local_ai_orbs.py  (writes the SVG + canvas in Shared\\Maps)
It rebuilds the SVG, then copies the page (wrapped for GitHub Pages) and the SVG into this repo, then runs the public check.
"""
import pathlib, re, shutil, subprocess, sys
REPO = pathlib.Path(__file__).resolve().parents[1]
MAPS = pathlib.Path(r"C:\AI Workspace\Shared\Maps")
DEST = REPO / "diagrams" / "local-ai-overview"
subprocess.run([sys.executable, r"C:\AI Workspace\Claude\tools\build_local_ai_orbs.py"], check=True)
body = (MAPS / "local-ai-overview.html").read_text(encoding="utf-8")
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="Floating-orb map of a home PC\'s free local AI models and where their results go.">\n')
page = head + re.sub(r"</style>", "body{margin:0}</style>\n</head>\n<body>", body, count=1) + "\n</body>\n</html>\n"
DEST.mkdir(parents=True, exist_ok=True)
(DEST / "index.html").write_text(page, encoding="utf-8")
shutil.copyfile(MAPS / "Local AI overview.svg", DEST / "overview.svg")
print("updated", DEST)
sys.exit(subprocess.run([sys.executable, str(REPO / "tools" / "check_public.py")]).returncode)
