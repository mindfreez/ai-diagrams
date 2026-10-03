"""Writes Shared\\Maps\\Local AI overview.svg (animated floating-orb map) and points 'Local AI overview.canvas' at it."""
import json
SVG = r"C:\AI Workspace\Shared\Maps\Local AI overview.svg"
CANVAS = r"C:\AI Workspace\Shared\Maps\Local AI overview.canvas"
W, H = 1960, 1330
# id: (x, y, radius, emoji, title, subtitle, gradient, [detail lines: "name|detail"])
orbs = {
    "you":    (230, 640, 96, "🤖", "You + assistants", "ask from the laptop or home PC", "violet",
               ["Claude|Opus / Sonnet · Code tab", "ChatGPT|Codex agent", "Scripts|scheduled overnight jobs"]),
    "text":   (760, 330, 64, "📝", "Text", "Ollama · via meter :11435", "green",
               ["qwen3:8b|5.2 GB · 4.4 tok/s · general", "qwen2.5-coder:7b|4.7 GB · 5 tok/s · code", "nemotron-3.5-lightning|25 GB · 5.8 tok/s · best quality (MoE)", "nomic-embed-text|0.3 GB · search by meaning"]),
    "img":    (1200, 330, 64, "🖼️", "Images", "512 px, CPU only", "green",
               ["FastSD CPU|SD-Turbo · OpenVINO · 12 s warm", "stable-diffusion.cpp|SD-Turbo + TAESD · 16 s"]),
    "vid":    (760, 660, 64, "🎬", "Video", "text → short clip", "green",
               ["Wan2.1 T2V 1.3B|~40 min per 1-s clip · 448×256", "Wan2.2 TI2V 5B|optional · weak at small sizes"]),
    "voice":  (1200, 660, 64, "🎙️", "Voice", "offline speech", "green",
               ["faster-whisper base.en|speech→text · 1.3 s/sentence", "Piper lessac-medium|text→speech · 14× realtime"]),
    "dash":   (760, 990, 64, "📊", "Usage dashboard", "Shared\\dashboards\\local-ai.html", "cyan",
               ["Ollama meter|tokens per model + assistant", "Refresh|every 15 min"]),
    "b3d":    (1200, 990, 64, "🧊", "3D", "Blender 5.2.2 + MCP", "green",
               ["car_modely.py|CorTek widebody Model Y", "Output|car-modely.glb · 30.7k tris"]),
    "shared": (1740, 330, 80, "☁️", "Shared folder", "Google Drive → laptop", "amber",
               ["rclone bisync|home 10 min · laptop 30 min"]),
    "chat":   (1740, 660, 80, "💬", "In chat", "shown inline", "amber",
               ["Images|≤800 px JPEG · full-res kept", "Clips|small mp4"]),
    "git":    (1740, 990, 80, "🐙", "GitHub", "code + 3D models", "amber",
               ["mindfreez/cortek-tour|push only when asked"]),
}
grads = {"violet": ("#c4a8ff", "#6b3fd4", "#8b5cf6"), "green": ("#9ff5c8", "#1f8f5a", "#34d399"),
         "cyan": ("#a5f0ff", "#1b7fa0", "#38bdf8"), "amber": ("#ffd9a0", "#c2410c", "#fb923c")}
HX, HY, HR = 980, 660, 470                                     # home-PC halo
flows = [("you", (HX - HR + 10, HY), "asks"), ((HX + HR - 10, HY - 90), "shared", ""), ((HX + HR - 10, HY), "chat", "results"),
         ((HX + HR - 10, HY + 90), "git", "")]
def pt(p): return (orbs[p][0], orbs[p][1]) if isinstance(p, str) else p

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, system-ui, sans-serif">',
       "<defs>",
       '<radialGradient id="bg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#1a2233"/><stop offset="1" stop-color="#07090f"/></radialGradient>',
       '<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#34d399" stop-opacity=".16"/><stop offset=".7" stop-color="#34d399" stop-opacity=".05"/><stop offset="1" stop-color="#34d399" stop-opacity="0"/></radialGradient>',
       '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
       '<filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>']
for g, (hi, lo, _) in grads.items():
    out.append(f'<radialGradient id="g-{g}" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{lo}"/><stop offset="1" stop-color="#0b0f18"/></radialGradient>')
out.append("""</defs><style>
.float{animation:bob 6s ease-in-out infinite}.f2{animation-duration:7.3s;animation-delay:-2s}.f3{animation-duration:8.1s;animation-delay:-4s}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.flow{fill:none;stroke-width:3;stroke-dasharray:2 14;stroke-linecap:round;animation:dash 1.6s linear infinite;opacity:.85}
@keyframes dash{to{stroke-dashoffset:-32}}
.halo{animation:pulse 5s ease-in-out infinite;transform-origin:980px 660px}@keyframes pulse{50%{transform:scale(1.04);opacity:.8}}
.t{fill:#f1f5f9;font-size:21px;font-weight:600;text-anchor:middle}.s{fill:#94a3b8;font-size:15px;text-anchor:middle}
.e{font-size:44px;text-anchor:middle;dominant-baseline:central}.lab{fill:#cbd5e1;font-size:16px;font-style:italic}.d{fill:#cbd5e1;font-size:14.5px;text-anchor:middle}.m{fill:#6ee7b7;font-weight:600}
</style>""")
out.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
import random; random.seed(7)
out += [f'<circle cx="{random.randint(0, W)}" cy="{random.randint(0, H)}" r="{random.choice([.8, 1, 1.4])}" fill="#fff" opacity="{random.uniform(.15, .5):.2f}"/>' for _ in range(110)]
out.append('<text x="60" y="80" fill="#f8fafc" font-size="34" font-weight="700">Local AI at a glance</text>')
out.append('<text x="60" y="114" fill="#94a3b8" font-size="17">Everything in the green cloud runs free on the home PC’s CPU — no cloud usage</text>')
out.append('<g class="halo"><circle cx="980" cy="660" r="470" fill="url(#halo)"/><circle cx="980" cy="660" r="470" fill="none" stroke="#34d399" stroke-opacity=".25" stroke-dasharray="4 10"/></g>')
out.append('<text x="980" y="176" class="s" style="fill:#6ee7b7;font-size:17px;letter-spacing:2px">HOME PC · LOCAL AI</text>')
for a, b, lab in flows:
    (x1, y1), (x2, y2) = pt(a), pt(b); mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 60
    color = "#a78bfa" if a == "you" else "#fb923c"
    out.append(f'<path class="flow" stroke="{color}" d="M{x1},{y1} Q{mx},{my} {x2},{y2}"/>')
    if lab: out.append(f'<text x="{mx:.0f}" y="{my + 18:.0f}" class="lab" text-anchor="middle">{lab}</text>')
for k, (i, (x, y, r, emo, title, sub, g, det)) in enumerate(orbs.items()):
    glow = grads[g][2]
    out.append(f'<g class="float f{k % 3 + 1}">'
               f'<circle cx="{x}" cy="{y}" r="{r + 10}" fill="{glow}" opacity=".22" filter="url(#glow)"/>'
               f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#g-{g})"/>'
               f'<ellipse cx="{x - r * .3}" cy="{y - r * .42}" rx="{r * .38}" ry="{r * .2}" fill="#fff" opacity=".28" filter="url(#soft)"/>'
               f'<text x="{x}" y="{y}" class="e" style="font-size:{int(r * .7)}px">{emo}</text>'
               f'<text x="{x}" y="{y + r + 30}" class="t">{title}</text><text x="{x}" y="{y + r + 52}" class="s">{sub}</text>'
               + "".join(f'<text x="{x}" y="{y + r + 80 + 21 * j}" class="d"><tspan class="m">{a}</tspan>  {b}</text>'
                         for j, (a, b) in enumerate(line.split("|", 1) for line in det))
               + "</g>")
out.append("</svg>")
open(SVG, "w", encoding="utf-8").write("\n".join(out))
json.dump({"nodes": [{"id": "map", "type": "file", "file": "Maps/Local AI overview.svg", "x": 0, "y": 0, "width": W, "height": H}], "edges": []},
          open(CANVAS, "w", encoding="utf-8"), indent=1)
print("wrote", SVG, "and", CANVAS)
