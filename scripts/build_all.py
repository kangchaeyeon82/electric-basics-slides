"""그림 → manim 영상 → pptx 조립을 한 번에. (영상 렌더링은 몇 분 걸림)

영상 건너뛰기: python scripts/build_all.py --no-videos
"""
import subprocess
import sys
from pathlib import Path

import make_figures
import build_deck

if __name__ == "__main__":
    make_figures.main()
    if "--no-videos" not in sys.argv:
        subprocess.run([sys.executable, str(Path(__file__).parent / "make_videos.py")], check=True)
    build_deck.main()
