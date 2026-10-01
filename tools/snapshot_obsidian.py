"""Makes the Obsidian copy of a diagram: a canvas that embeds the live desktop page, plus a PNG snapshot as the offline copy.
Usage: python tools/snapshot_obsidian.py <folder-name> "<Obsidian title>"
  e.g. python tools/snapshot_obsidian.py assistant-rules "Assistant rules"
Writes Shared\\Maps\\<title>.png + .canvas (home PC vault) and diagrams/<folder>/<folder>.png + .canvas (repo vault).
Uses headless Edge (no installs); the page height is found by trimming the dark background at the bottom."""
import json, pathlib, shutil, subprocess, sys, tempfile
REPO = pathlib.Path(__file__).resolve().parents[1]
MAPS = pathlib.Path(r"C:\AI Workspace\Shared\Maps")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WIDTH = 1400                                                            # desktop layout (zones side by side)
SCALE = 2                                                               # crisp offline PNG

def shoot(url, out, height, scale):
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
                    f"--window-size={WIDTH},{height}", "--virtual-time-budget=4000", f"--screenshot={out}", url], check=True, capture_output=True)

def content_bottom(png):
    """Last row (in CSS px) that has bright pixels, via System.Drawing so nothing needs installing."""
    ps = f"""Add-Type -AssemblyName System.Drawing; $b=[Drawing.Bitmap]::FromFile('{png}'); $last=0
for($y=0;$y -lt $b.Height;$y+=4){{ $n=0; for($x=0;$x -lt $b.Width;$x+=5){{ $c=$b.GetPixel($x,$y); if(($c.R+$c.G+$c.B) -gt 230){{$n++}} }}; if($n -ge 3){{$last=$y}} }}
$b.Dispose(); $last"""
    return int(subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, check=True).stdout.strip())

def main(name, title):
    page = REPO / "diagrams" / name / "index.html"
    with tempfile.TemporaryDirectory() as t:
        probe = pathlib.Path(t) / "probe.png"; shoot(page.as_uri(), probe, 4000, 1)
        height = content_bottom(probe) + 64
    png = MAPS / f"{title}.png"; shoot(page.as_uri(), png, height, SCALE)
    shutil.copyfile(png, page.parent / f"{name}.png")
    live = f"https://mindfreez.github.io/ai-diagrams/diagrams/{name}/"
    # The canvas shows the live page itself (a web embed: same look and animation as GitHub Pages, desktop width).
    # The PNG is the offline copy; Obsidian's canvas mis-draws large images on this PC's GPU, so it isn't the main view.
    canvas = lambda file: json.dumps({"nodes": [
        {"id": "live", "type": "link", "url": live, "x": 0, "y": 0, "width": WIDTH, "height": height},
        {"id": "offline", "type": "text", "x": 0, "y": height + 40, "width": WIDTH, "height": 60,
         "text": f"Offline copy: [[{file}]] · live page: {live}"}], "edges": []}, indent=1)
    (MAPS / f"{title}.canvas").write_text(canvas(f"Maps/{title}.png"), encoding="utf-8")
    (page.parent / f"{name}.canvas").write_text(canvas(f"diagrams/{name}/{name}.png"), encoding="utf-8")
    print(f"snapshot {WIDTH}x{height} -> {png}")

if __name__ == "__main__":
    main(*sys.argv[1:3])
