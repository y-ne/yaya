import time
from adbutils import adb

YOUTUBE_URL = "https://youtu.be/3QFxq-P2WgA?si=hwhY_cF6_t8vcZ2T"
YOUTUBE_PACKAGE = "com.google.android.youtube"


def get_device():
    devices = adb.device_list()
    if not devices:
        raise RuntimeError("No devices found. Make sure at least one device is connected and authorized.")

    if len(devices) > 1:
        print("Multiple devices detected, using the first one:")

    d = devices[0]

    try:
        state = d.get_state()
    except Exception:
        state = "unknown"

    print(f"Using device: {d.serial} (state={state})")
    return d


def open_youtube_video(d, url: str):
    cmd = (
        "am start -S "
        "-a android.intent.action.VIEW "
        f"-d '{url}' "
        f"{YOUTUBE_PACKAGE}"
    )
    print("Running:", cmd)
    d.shell(cmd)


def close_youtube_and_home(d):
    print("Force-stopping YouTube…")
    d.shell(f"am force-stop {YOUTUBE_PACKAGE}")

    print("Going to HOME…")
    d.shell("input keyevent KEYCODE_HOME")


def main():
    d = get_device()

    print(f"Opening video: {YOUTUBE_URL}")
    open_youtube_video(d, YOUTUBE_URL)

    print("Waiting 10 seconds…")
    time.sleep(10)

    close_youtube_and_home(d)
    print("Done.")


if __name__ == "__main__":
    main()
