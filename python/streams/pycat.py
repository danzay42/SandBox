from pathlib import Path
import sys
import argparse
from typing import NamedTuple


class Arguments(NamedTuple):
    file_in: Path | None = None
    file_out: Path | None = None


def parse_cli() -> Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="file_in", type=Path)
    parser.add_argument("-o", dest="file_out", type=Path)
    return Arguments(**vars(parser.parse_args()))


def main():
    args = parse_cli()

    input_stream = args.file_in.open(encoding="utf-8") if args.file_in else sys.stdin
    output_stream = args.file_out.open("w", encoding="utf-8") if args.file_out else sys.stdout

    for line in input_stream:
        print(f"processed: {line}", file=output_stream)


if __name__ == "__main__":
    main()
