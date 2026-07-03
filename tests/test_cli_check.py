import sys

import pytest

from edt.cli import main


def test_check_cli_exits_zero_when_no_issues(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["edt", "check"])
    monkeypatch.setattr("edt.cli.check_project", lambda root: [])

    with pytest.raises(SystemExit) as exit_info:
        main()

    assert exit_info.value.code == 0
    assert capsys.readouterr().out == ""


def test_check_cli_exits_nonzero_and_prints_issues(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["edt", "check"])
    monkeypatch.setattr(
        "edt.cli.check_project",
        lambda root: ["validation errors: 1", "document is not publication ready"],
    )

    with pytest.raises(SystemExit) as exit_info:
        main()

    assert exit_info.value.code == 1
    assert capsys.readouterr().out == (
        "validation errors: 1\n"
        "document is not publication ready\n"
    )
