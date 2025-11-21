
from pathlib import Path
from time import perf_counter
from adbutils import adb


def main():
    devices = adb.device_list()
    if not devices:
        raise RuntimeError("No devices found. Make sure at least one device is connected and authorized.")

    out_dir = Path("pictures")
    out_dir.mkdir(exist_ok=True)

    total_start = perf_counter()

    for d in devices:
        serial = d.serial
        print(f"\n=== Device: {serial} ===")

        start = perf_counter()
        img = d.screenshot()  # grab screenshot
        out_path = out_dir / f"{serial}.png"
        img.save(out_path)
        end = perf_counter()

        duration = end - start
        print(f"Saved: {out_path}")
        print(f"Time for {serial}: {duration:.3f} seconds")

    total_end = perf_counter()
    total_duration = total_end - total_start
    print(f"\nAll done in {total_duration:.3f} seconds.")


if __name__ == "__main__":
    main()
