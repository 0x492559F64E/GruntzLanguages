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
        description="Extract .resx resource values and IDs into separate files."
    )
    parser.add_argument("input", type=Path, help="Input .resx file")
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Values output file (defaults to extracted_values.txt in the current directory)",
    )
    args = parser.parse_args()

    values_output_path = args.output or Path("extracted_values.txt")
    id_output_path = values_output_path.with_name(
        f"{values_output_path.stem}_ID{values_output_path.suffix}"
    )
    output_path = append_sync_version(values_output_path)
    id_output_path = append_sync_version(id_output_path)
    root = ET.parse(args.input).getroot()
    values = []
    ids = []
    for data in root.iter():
        if data.tag.rsplit("}", 1)[-1] != "data":
            continue
        value = data.find("{*}value")
        if value is None:
            continue
        ids.append(data.get("name", ""))
        values.append(" ".join((value.text or "").splitlines()))

    output_path.write_text("\n".join(values) + "\n", encoding="utf-8")
    id_output_path.write_text("\n".join(ids) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()