from pathlib import Path
from PIL import Image


SCRIPT_DIR = Path(__file__).resolve().parent


def convert_webp_to_jpg(webp_path: Path) -> Path:
    jpg_path = webp_path.with_suffix(".jpg")

    with Image.open(webp_path) as img:
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            img = img.convert("RGBA")
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            rgb_img = background
        else:
            rgb_img = img.convert("RGB")

        rgb_img.save(
            jpg_path,
            format="JPEG",
            quality=100,
            subsampling=0,
            optimize=True,
            progressive=True,
        )

    return jpg_path


def main() -> None:
    webp_files = [
        p for p in SCRIPT_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() == ".webp"
    ]

    if not webp_files:
        print(f"No .webp files in: {SCRIPT_DIR}")
        return

    ok, failed = 0, 0
    for webp_file in webp_files:
        try:
            jpg_file = convert_webp_to_jpg(webp_file)
            webp_file.unlink()
            print(f"[OK] {webp_file.relative_to(SCRIPT_DIR)} -> {jpg_file.name}")
            ok += 1
        except Exception as e:
            print(f"[ERR] {webp_file.relative_to(SCRIPT_DIR)}: {e}")
            failed += 1

    print(f"\nSuccess: {ok}, issues: {failed}")


if __name__ == "__main__":
    main()
