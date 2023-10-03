import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class Arguments:
    file_in: Path | None = None
    file_out: Path | None = None

    @classmethod
    def from_arguments(cls, argv: Sequence[str] | None = None) -> "Arguments":
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", dest="file_in", type=Path)
        parser.add_argument("-o", dest="file_out", type=Path)
        return cls(**vars(parser.parse_args(argv)))


def main(argv: Sequence[str] | None = None):
    args = Arguments.from_arguments(argv)

    input_stream = args.file_in.open(encoding="utf-8") if args.file_in else sys.stdin
    output_stream = (
        args.file_out.open("w", encoding="utf-8") if args.file_out else sys.stdout
    )

    for line in input_stream:
        print(f"processed: {line.strip()}", file=output_stream, flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
