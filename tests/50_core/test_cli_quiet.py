# tests/50_core/test_cli_quiet.py
"""Tests for --quiet CLI parameter."""

from pathlib import Path

import pytest

import zipbundler.logs as mod_logs
import zipbundler.main as mod_main


ARGPARSE_ERROR_EXIT_CODE = 2


def test_quiet_flag_sets_log_level(
    tmp_path: Path,
) -> None:
    """Should set log level to warning when --quiet is used."""
    # Create a test package
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")

    output = tmp_path / "app.pyz"

    # Handle both module and function cases (runtime mode swap)
    main_func = mod_main if callable(mod_main) else mod_main.main
    # Call main with --quiet flag
    code = main_func([str(pkg_dir), "-o", str(output), "--quiet"])

    # Verify build succeeded
    assert code == 0
    assert output.exists()

    # Verify logger level was set to warning
    logger = mod_logs.getAppLogger()
    assert logger.levelName.upper() == "WARNING"


def test_quiet_flag_suppresses_info_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Should suppress info-level output when --quiet is used."""
    # Create a test package
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")

    output = tmp_path / "app.pyz"

    # Handle both module and function cases (runtime mode swap)
    main_func = mod_main if callable(mod_main) else mod_main.main
    # Call main with --quiet flag
    code = main_func([str(pkg_dir), "-o", str(output), "--quiet"])

    # Verify build succeeded
    assert code == 0
    assert output.exists()

    # Check that info messages are suppressed (quiet sets to warning)
    captured = capsys.readouterr()
    out = captured.out.lower()
    # Info-level messages like "Created zipapp" should not appear
    assert "created zipapp" not in out


def test_verbose_and_quiet_mutually_exclusive(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Should fail when both --verbose and --quiet are provided."""
    # Create a test package
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")

    output = tmp_path / "app.pyz"

    # Handle both module and function cases (runtime mode swap)
    main_func = mod_main if callable(mod_main) else mod_main.main
    # argparse should exit with SystemExit(2)
    with pytest.raises(SystemExit) as e:
        main_func([str(pkg_dir), "-o", str(output), "--quiet", "--verbose"])

    assert e.value.code == ARGPARSE_ERROR_EXIT_CODE

    # Verify error message mentions the conflict
    captured = capsys.readouterr()
    combined = (captured.out + captured.err).lower()
    assert "not allowed with argument" in combined or "mutually exclusive" in combined


def test_log_level_flag_works(
    tmp_path: Path,
) -> None:
    """Should set log level when --log-level is used."""
    # Create a test package
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")

    output = tmp_path / "app.pyz"

    # Handle both module and function cases (runtime mode swap)
    main_func = mod_main if callable(mod_main) else mod_main.main
    # Call main with --log-level flag
    code = main_func([str(pkg_dir), "-o", str(output), "--log-level", "debug"])

    # Verify build succeeded
    assert code == 0
    assert output.exists()

    # Verify logger level was set to debug
    logger = mod_logs.getAppLogger()
    assert logger.levelName.upper() == "DEBUG"
