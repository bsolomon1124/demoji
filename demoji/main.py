import argparse
import io
import sys

from demoji import replace_with_desc


def demojify(fp: io.IOBase):
    for line in fp:
        print(replace_with_desc(line), end="")


def main():
    if not sys.stdin.isatty():
        if "-h" not in sys.argv and "--help" not in sys.argv:
            fp = sys.stdin
            return demojify(fp)

    parser = argparse.ArgumentParser(
        description=(
            "Replace emojis in file(s) or string"
            " with their :code: equivalents"
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
    files = args.files
    for filename in files:
        if filename == "-":
            fp = sys.stdin
            demojify(fp)
        else:
            with open(filename) as fp:
                demojify(fp)


if __name__ == "__main__":
    main()
