"""make.fun entry for "Sum up 26 November's world news in one image".

The program writes one image to /output/entry.png. The image itself is the
entry.png stored beside this file (an illustrated front page of 37 stories
drawn by generate_image_v2.py from the day's reported news; v1 used
generate_image.py), and this program simply copies it, byte for byte, so two runs
always produce identical output. Standard library only; no network.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    # The gate accepts at most 1 MiB; fail loudly rather than write a bad entry.
    assert target.stat().st_size <= 1024 * 1024, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
