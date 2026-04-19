import io
import subprocess
import sys

import pytest

from demoji.main import demojify, main


class _FakeStdin(io.StringIO):
    def __init__(self, data: str, isatty: bool) -> None:
        super().__init__(data)
        self._isatty = isatty

    def isatty(self) -> bool:
        return self._isatty


def _patch_cli(monkeypatch, *, stdin_data: str, isatty: bool, argv: list[str]) -> None:
    monkeypatch.setattr(sys, "stdin", _FakeStdin(stdin_data, isatty))
    monkeypatch.setattr(sys, "argv", argv)


def test_demojify_iterable(capsys):
    demojify(["All done! ✨ 🍰 ✨\n", "we didnt start the 🔥\n"])
    out = capsys.readouterr().out
    assert out == (
        "All done! :sparkles: :shortcake: :sparkles:\nwe didnt start the :fire:\n"
    )


def test_main_reads_piped_stdin(monkeypatch, capsys):
    _patch_cli(monkeypatch, stdin_data="hi 🔥\n", isatty=False, argv=["demoji"])
    main()
    assert capsys.readouterr().out == "hi :fire:\n"


def test_main_reads_from_file(tmp_path, monkeypatch, capsys):
    f = tmp_path / "sample.txt"
    f.write_text("All done! ✨ 🍰 ✨\n", encoding="utf-8")
    _patch_cli(monkeypatch, stdin_data="", isatty=True, argv=["demoji", str(f)])
    main()
    assert capsys.readouterr().out == "All done! :sparkles: :shortcake: :sparkles:\n"


def test_main_dash_reads_stdin(monkeypatch, capsys):
    # isatty True so we fall through to argparse, which then handles "-".
    _patch_cli(
        monkeypatch,
        stdin_data="we didnt start the 🔥\n",
        isatty=True,
        argv=["demoji", "-"],
    )
    main()
    assert capsys.readouterr().out == "we didnt start the :fire:\n"


def test_main_help_exits(monkeypatch, capsys):
    _patch_cli(monkeypatch, stdin_data="", isatty=False, argv=["demoji", "-h"])
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 0
    assert "Replace emojis" in capsys.readouterr().out


def test_module_entrypoint():
    # Smoke test of `python -m demoji` wiring.
    result = subprocess.run(
        [sys.executable, "-m", "demoji"],
        input="All done! ✨\n",
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "All done! :sparkles:\n"
