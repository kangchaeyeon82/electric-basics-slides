"""scripts/figures/fig_*.py 를 모두 실행해 assets/ 에 그림을 다시 만든다.

특정 섹션만: python scripts/make_figures.py 03 07
"""
import subprocess
import sys
from pathlib import Path

FIG_SCRIPTS = Path(__file__).resolve().parent / "figures"


def main(only=()):
    scripts = sorted(FIG_SCRIPTS.glob("fig_*.py"))
    if only:
        scripts = [p for p in scripts if any(p.stem.startswith(f"fig_{k}") for k in only)]
    failed = []
    for p in scripts:
        print(f"[그림] {p.name}")
        if subprocess.run([sys.executable, str(p)]).returncode != 0:
            failed.append(p.name)
    if failed:
        sys.exit(f"실패: {', '.join(failed)}")


if __name__ == "__main__":
    main(sys.argv[1:])
