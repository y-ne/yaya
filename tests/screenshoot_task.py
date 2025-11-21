from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from adbutils import adb
from PIL import Image


TARGET_HEIGHT = 720
JPEG_QUALITY = 70


def main():
    devices = adb.device_list()
    if not devices:
        raise RuntimeError("No devices found.")

    out_dir = Path("pictures")
    out_dir.mkdir(exist_ok=True)

    def shoot(d):
        serial = d.serial
        start = perf_counter()

        img = d.screenshot()

        w, h = img.size
        if h > TARGET_HEIGHT:
            scale = TARGET_HEIGHT / h
            new_w = int(w * scale)
            new_h = TARGET_HEIGHT
            img = img.resize((new_w, new_h), Image.LANCZOS)

        img = img.convert("L")

        out_path = out_dir / f"{serial}.jpg"
        img.save(out_path, "JPEG", quality=JPEG_QUALITY)

        duration = perf_counter() - start
        print(f"{serial}: saved to {out_path} ({img.size[0]}x{img.size[1]}, grayscale) in {duration:.3f}s")

    total_start = perf_counter()

    with ThreadPoolExecutor(max_workers=len(devices)) as pool:
        pool.map(shoot, devices)

    total_duration = perf_counter() - total_start
    print(f"All screenshots done in {total_duration:.3f}s.")


if __name__ == "__main__":
    main()
