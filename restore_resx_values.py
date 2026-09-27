import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape


VALUE_PATTERN = re.compile(
	r"<!--.*?-->|(<value\b[^>]*>)(.*?)(</value>)", re.DOTALL
)
DATA_PATTERN = re.compile(
	r"<!--.*?-->|(<data\b[^>]*>)(.*?)(</data\s*>)", re.DOTALL
)


def main():
	parser = argparse.ArgumentParser(
		description="Restore data values from a text file, one value per line."
	)
	parser.add_argument("input", type=Path, help="Original .resx file")
	parser.add_argument("values", type=Path, help="Text file with one value per line")
	parser.add_argument(
		"output",
		nargs="?",
		type=Path,
		help="Output .resx file (defaults to <input>.filled.resx)",
	)
	args = parser.parse_args()

	xml_text = args.input.read_text(encoding="utf-8")
	root = ET.fromstring(xml_text)
	values = args.values.read_text(encoding="utf-8").splitlines()
	data_values = [
		child
		for data in root.iter()
		if data.tag.rsplit("}", 1)[-1] == "data"
		for child in data
		if child.tag.rsplit("}", 1)[-1] == "value"
	]
	if len(values) != len(data_values):
		parser.error(
			f"The text file has {len(values)} lines, but the input .resx has "
			f"{len(data_values)} <value> elements inside <data> entries."
		)

	value_index = 0

	def replace_data(match):
		nonlocal value_index
		if match.group(1) is None:
			return match.group(0)

		def replace_value(value_match):
			nonlocal value_index
			if value_match.group(1) is None:
				return value_match.group(0)
			replacement = escape(values[value_index])
			value_index += 1
			return (
				f"{value_match.group(1)}{replacement}{value_match.group(3)}"
			)

		body = VALUE_PATTERN.sub(replace_value, match.group(2))
		return f"{match.group(1)}{body}{match.group(3)}"

	updated_xml = DATA_PATTERN.sub(replace_data, xml_text)
	if value_index != len(values):
		parser.error("Could not locate every <value> inside a <data> entry.")
	ET.fromstring(updated_xml)

	output_path = args.output or args.input.with_name(
		f"{args.input.stem}.filled{args.input.suffix}"
	)
	output_path.write_text(updated_xml, encoding="utf-8")


if __name__ == "__main__":
	main()
