from pathlib import Path
from time import sleep, perf_counter

import cv2
import numpy as np
from adbutils import adb

BASE_DIR = Path(__file__).resolve().parent.parent
ICON_PATH = BASE_DIR / "icons" / "hyperos_close_all_recent_app.jpg"
PICTURES_DIR = BASE_DIR / "pictures"

MATCH_THRESHOLD = 0.7


def load_template():
    print(f"Loading template from: {ICON_PATH}")
    tpl = cv2.imread(str(ICON_PATH), cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        raise RuntimeError(f"Could not load template image at {ICON_PATH}")
    return tpl


def pil_to_gray_cv2(pil_image):
    arr = np.array(pil_image)
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray


def capture_recents_screenshot(device):
    device.shell("input keyevent KEYCODE_HOME")
    sleep(0.3)

    device.shell("input keyevent KEYCODE_APP_SWITCH")
    sleep(0.7)

    pil_img = device.screenshot()
    gray = pil_to_gray_cv2(pil_img)
    return gray, pil_img


def find_best_match(gray_img, tpl, serial):
    res = cv2.matchTemplate(gray_img, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    h, w = tpl.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cx = top_left[0] + w // 2
    cy = top_left[1] + h // 2

    print(
        f"{serial}: best match score = {max_val:.3f}, "
        f"top_left={top_left}, bottom_right={bottom_right}, center=({cx}, {cy})"
    )

    return cx, cy, max_val, top_left, bottom_right


def save_annotated_screenshot(serial, pil_img, top_left, bottom_right, score):
    PICTURES_DIR.mkdir(exist_ok=True)

    img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    cv2.rectangle(img_bgr, top_left, bottom_right, (255, 255, 255), 2)
    cv2.putText(
        img_bgr,
        f"{score:.3f}",
        (top_left[0], max(0, top_left[1] - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    out_path = PICTURES_DIR / f"{serial}.png"
    cv2.imwrite(str(out_path), img_bgr)
    print(f"{serial}: annotated screenshot saved to {out_path}")


def tap(device, x, y):
    device.shell(f"input tap {x} {y}")


def clear_recents_for_device(device, tpl):
    serial = device.serial
    print(f"\n=== {serial}: clearing recent apps ===")
    start = perf_counter()

    gray, pil_img = capture_recents_screenshot(device)
    cx, cy, score, top_left, bottom_right = find_best_match(gray, tpl, serial)

    save_annotated_screenshot(serial, pil_img, top_left, bottom_right, score)

    if score < MATCH_THRESHOLD:
        duration = perf_counter() - start
        print(
            f"{serial}: score {score:.3f} < threshold {MATCH_THRESHOLD:.3f}, "
            f"NOT tapping. Took {duration:.3f}s."
        )
        return

    print(f"{serial}: Tapping center=({cx}, {cy}), score={score:.3f} …")
    tap(device, cx, cy)
    sleep(0.5)

    duration = perf_counter() - start
    print(f"{serial}: Done in {duration:.3f}s.")


def main():
    tpl = load_template()

    print("Listing devices...")
    devices = adb.device_list()
    if not devices:
        raise RuntimeError("No devices found. Connect at least one device via ADB.")

    print(f"Found {len(devices)} device(s).")

    total_start = perf_counter()
    for d in devices:
        clear_recents_for_device(d, tpl)
    total_duration = perf_counter() - total_start

    print(f"\nAll devices processed in {total_duration:.3f}s.")


if __name__ == "__main__":
    main()
