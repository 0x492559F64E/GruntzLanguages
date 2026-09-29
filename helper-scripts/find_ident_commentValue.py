import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


SYNC_VERSION_PATH = Path(__file__).resolve().parent.parent / "syncversion.txt"


def append_sync_version(path: Path) -> Path:
    try:
        version = "_".join(SYNC_VERSION_PATH.read_text(encoding="utf-8").split())
    except FileNotFoundError:
        return path
    if not version:
        return path
    return path.with_name(f"{path.stem}_{version}{path.suffix}")


def main():
    parser = argparse.ArgumentParser(
        description="List .resx data nodes whose value matches their comment."
    )
    parser.add_argument("input", type=Path, help="Input .resx file")
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Values output file (defaults to <input-stem>_ident_commentValue.txt in the current directory)",
    )
    args = parser.parse_args()

    root = ET.parse(args.input).getroot()
    ids = []
    values = []
    for data in root.iter():
        if data.tag.rsplit("}", 1)[-1] != "data":
            continue

        value = data.find("{*}value")
        comment = data.find("{*}comment")
        if value is None or comment is None:
            continue

        value_text = "".join(value.itertext())
        comment_text = "".join(comment.itertext())
        if value_text == comment_text:
            ids.append(data.get("name", ""))
            values.append(value_text)

    values_output_path = args.output or Path(
        f"{args.input.stem}_ident_commentValue.txt"
    )
    id_output_path = values_output_path.with_name(
        f"{values_output_path.stem}_ID{values_output_path.suffix}"
    )
    values_output_path = append_sync_version(values_output_path)
    id_output_path = append_sync_version(id_output_path)
    values_output_path.write_text(
        "\n".join(values) + ("\n" if values else ""), encoding="utf-8"
    )
    id_output_path.write_text(
        "\n".join(ids) + ("\n" if ids else ""), encoding="utf-8"
    )
    print(f"Saved {len(ids)} matches to {id_output_path} and {values_output_path}")


if __name__ == "__main__":
    main()