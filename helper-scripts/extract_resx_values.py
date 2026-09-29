import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Extract .resx resource values and IDs into separate files."
    )
    parser.add_argument("input", type=Path, help="Input .resx file")
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Values output file (defaults to extracted_values.txt)",
    )
    args = parser.parse_args()

    output_path = args.output or Path("extracted_values.txt")
    id_output_path = output_path.with_name(
        f"{output_path.stem}_ID{output_path.suffix}"
    )
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