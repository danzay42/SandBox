from pathlib import Path
import re


def build_row(line: str) -> str:
    result = re.match(
        r"^\d*\.\s*" +
        r"(?P<title>[ёЁA-я\w\s\.:…&,-]*?)" +
        r"(?P<edition>\s*(?P<edition_num>\d*)-?[ёЁA-я\a]*\s*(?:(?:e|E)d|(?:И|и)зд)[\wёЁA-я\.,]*)?" +
        r"(?:\s*::\s*(?P<author>[ёЁA-я\w\s\.,-]*?))?" +
        r"(?:\((?P<note>[ёЁA-я\w\s,]*)\))?" +
        r"\s*$",
        line).groupdict(default="")
    result["edition_num"] = result["edition_num"] or result["edition"]
    result["title"] = result["title"].strip(".,")
    return "{title} | {author} | {edition_num} |  | {note}".format(**result).strip("| ")


def build_header(line: str) -> list[str]:
    header = re.match(r"\W*([\w\s,]*)\W*", line).groups()[0].strip()
    return [
        "",
        "",
        f"# {header}",
        "",
        "Название | Автор | Изд | Год | Заметка",
        ":-: | --- | :-: | :-: | ---"
    ]


def parse(line: str) -> list[str]:
    if line.startswith("#"):
        return build_header(line)
    return [build_row(line)]


def main():
    file = Path("Книги/ИТ.md")
    content = file.read_text().splitlines()
    new_content = []

    for line in content:
        if not line:
            continue
        new_content += parse(line)

    new_file = Path("Книги/ИТ_new.md")
    new_file.write_text("\n".join(new_content))


if __name__ == "__main__":
    main()