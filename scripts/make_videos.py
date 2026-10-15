"""scripts/manim/scenes.py 의 장면을 렌더링해 assets/videos/ 에 mp4 + 포스터 PNG 로 저장한다.

전부:   python scripts/make_videos.py
하나만: python scripts/make_videos.py m03_ohm_graph
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENES_FILE = ROOT / "scripts" / "manim" / "scenes.py"
MEDIA = ROOT / ".cache" / "manim"
OUT = ROOT / "assets" / "videos"

SCENES = ["m01_electron_flow", "m03_ohm_graph", "m06_dc_ac", "m07_capacitor", "m09_charger_waveforms"]


def render(name, still=False):
    cmd = [sys.executable, "-m", "manim", "render", "--disable_caching", "--media_dir", str(MEDIA),
           "-o", name, str(SCENES_FILE), name]
    cmd.insert(4, "-s" if still else "-qh")
    # 해상도·프레임은 scenes.py 의 config 를 쓴다 (-qh 는 기본 품질 플래그일 뿐)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:], sep="\n")
        raise RuntimeError(f"{name} 렌더링 실패")
    pattern = f"**/{name}.png" if still else f"**/{name}.mp4"
    found = sorted(MEDIA.glob(pattern), key=lambda p: p.stat().st_mtime)
    if not found:
        raise RuntimeError(f"{name}: 결과 파일을 찾지 못함")
    return found[-1]


def main(only=()):
    OUT.mkdir(parents=True, exist_ok=True)
    names = [n for n in SCENES if not only or n in only]
    unknown = set(only) - set(SCENES)
    if unknown:
        sys.exit(f"알 수 없는 장면: {', '.join(sorted(unknown))}")
    failed = []
    for name in names:
        print(f"[영상] {name}")
        try:
            shutil.copy(render(name), OUT / f"{name}.mp4")
            shutil.copy(render(name, still=True), OUT / f"{name}.png")
            print(f"  saved {name}.mp4, {name}.png")
        except RuntimeError as e:
            print(f"  ! {e}")
            failed.append(name)
    if failed:
        sys.exit(f"실패: {', '.join(failed)}")


if __name__ == "__main__":
    main(sys.argv[1:])
