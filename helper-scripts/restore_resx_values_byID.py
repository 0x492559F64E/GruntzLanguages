import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape


SYNC_VERSION_PATH = Path(__file__).resolve().parent.parent / "syncversion.txt"


def append_sync_version(path: Path) -> Path:
    try:
        version = "_".join(SYNC_VERSION_PATH.read_text(encoding="utf-8").split())
    except FileNotFoundError:
        return path
    if not version:
        return path
    return path.with_name(f"{path.stem}_{version}{path.suffix}")


VALUE_PATTERN = re.compile(
    r"<!--.*?-->|(<value\b[^>]*>)(.*?)(</value>)", re.DOTALL
)
DATA_PATTERN = re.compile(
    r"<!--.*?-->|(<data\b[^>]*>)(.*?)(</data\s*>)", re.DOTALL
)


def main():
    parser = argparse.ArgumentParser(
        description="Restore translated values from separate value and ID files."
    )
    parser.add_argument("input", type=Path, help="Original .resx file")
    parser.add_argument("values", type=Path, help="Text file with one value per line")
    parser.add_argument("ids", type=Path, help="Text file with one resource ID per line")
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Output .resx file (defaults to <input-stem>.filled.resx in the current directory)",
    )
    args = parser.parse_args()

    xml_text = args.input.read_text(encoding="utf-8")
    root = ET.fromstring(xml_text)
    values = args.values.read_text(encoding="utf-8").splitlines()
    ids = args.ids.read_text(encoding="utf-8").splitlines()
    if len(values) != len(ids):
        parser.error(
            f"The values file has {len(values)} lines, but the IDs file has "
            f"{len(ids)} lines."
        )

    translations = dict(zip(ids, values))
    if len(translations) != len(ids):
        parser.error("The IDs file contains duplicate resource names.")

    resource_names = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] != "data":
            continue
        if not any(child.tag.rsplit("}", 1)[-1] == "value" for child in element):
            continue
        name = element.get("name")
        if name is None:
            parser.error("A <data> element with a <value> is missing its name.")
        resource_names.append(name)

    if len(resource_names) != len(set(resource_names)):
        parser.error("The input .resx contains duplicate resource names.")
    unknown_names = translations.keys() - set(resource_names)
    missing_names = set(resource_names) - translations.keys()
    if unknown_names or missing_names:
        parser.error(
            f"Resource names do not match: {len(unknown_names)} unknown, "
            f"{len(missing_names)} missing."
        )

    seen_names = []

    def replace_data(match):
        if match.group(1) is None:
            return match.group(0)
        data = ET.fromstring(match.group(0))
        name = data.get("name")
        value_matches = [
            value_match
            for value_match in VALUE_PATTERN.finditer(match.group(2))
            if value_match.group(1)
        ]
        if name not in translations or len(value_matches) != 1:
            parser.error(f"Could not locate the value for resource {name!r}.")
        seen_names.append(name)
        body = VALUE_PATTERN.sub(
            lambda value_match: (
                f"{value_match.group(1)}{escape(translations[name])}{value_match.group(3)}"
                if value_match.group(1)
                else value_match.group(0)
            ),
            match.group(2),
            count=1,
        )
        return f"{match.group(1)}{body}{match.group(3)}"

    updated_xml = DATA_PATTERN.sub(replace_data, xml_text)
    if set(seen_names) != set(resource_names):
        parser.error("Could not locate every named <data> element in the input XML.")
    ET.fromstring(updated_xml)

    output_path = append_sync_version(
        args.output or Path(f"{args.input.stem}.filled{args.input.suffix}")
    )
    output_path.write_text(updated_xml, encoding="utf-8")


if __name__ == "__main__":
    main()