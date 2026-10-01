"""Pre-commit check for this PUBLIC repo: refuses likely secrets and private material. Exit code 1 = fix before committing.
Usage: python tools/check_public.py"""
import pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = {
    "API key / token": r"(sk-(ant-|proj-)?[\w-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|ya29\.[\w-]{20,}|1//0[\w-]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-[\w-]{10,})",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "password/secret assignment": r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[^\s'\"]{6,}",
    "email address": r"[\w.+-]+@(?!users\.noreply\.github\.com)[A-Za-z][\w-]*\.[A-Za-z]{2,}\b",
    "chat history": r"(?i)(History[\\/]Chats|Rule candidates|conversations\.json|\.jsonl\b)",
    "private marker": r"\b(PRIVATE:|CONFIDENTIAL|DO NOT PUBLISH)",   # explicit markers, uppercase
}
files = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True).stdout.split()
problems = []
for f in files:
    p = ROOT / f
    if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4"} or p.name == "check_public.py": continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    for label, pat in PATTERNS.items():
        for m in re.finditer(pat, text):
            line = text.count("\n", 0, m.start()) + 1
            problems.append(f"{f}:{line}: {label}: {m.group(0)[:40]}")
print("\n".join(problems) if problems else f"OK: {len(files)} files checked, nothing private found.")
sys.exit(1 if problems else 0)
