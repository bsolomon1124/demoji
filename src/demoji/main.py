import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

from demoji import replace_with_desc


def demojify(fp: Iterable[str]) -> None:
    for line in fp:
        print(replace_with_desc(line), end="")


def main() -> None:
    if not sys.stdin.isatty() and "-h" not in sys.argv and "--help" not in sys.argv:
        demojify(sys.stdin)
        return

    parser = argparse.ArgumentParser(
        description=(
            "Replace emojis in file(s) or string with their :code: equivalents"
        )
    )
    parser.add_argument(
        "files",
        nargs="+",
        help=(
            "One or more Python files to demoji-fy,"
            " or '-' for stdin; also accepts piped stdin"
        ),
    )
    args = parser.parse_args()
    for filename in args.files:
        if filename == "-":
            demojify(sys.stdin)
        else:
            with Path(filename).open(encoding="utf-8") as fp:
                demojify(fp)


if __name__ == "__main__":  # pragma: no cover
    main()
