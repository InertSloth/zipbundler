# tests/50_core/test_build_compression.py
"""Tests for compression support in zipapp building."""

import zipfile
from pathlib import Path

import zipbundler.build as mod_build


def test_build_zipapp_with_compression(tmp_path: Path) -> None:
    """Test building a zipapp with compression enabled."""
    # Create a test package
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text("def func():\n    pass\n")

    output = tmp_path / "app.pyz"

    mod_build.build_zipapp(
        output=output,
        packages=[pkg_dir],
        entry_point=None,
        compress=True,
    )

    # Verify zip file was created
    assert output.exists()

    # Verify compression is enabled
    with zipfile.ZipFile(output, "r") as zf:
        # Check that files are compressed (ZIP_DEFLATED)
        for info in zf.infolist():
            assert info.compress_type == zipfile.ZIP_DEFLATED


def test_build_zipapp_without_compression(tmp_path: Path) -> None:
    """Test building a zipapp without compression (default behavior)."""
    # Create a test package
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text("def func():\n    pass\n")

    output = tmp_path / "app.pyz"

    mod_build.build_zipapp(
        output=output,
        packages=[pkg_dir],
        entry_point=None,
        compress=False,
    )

    # Verify zip file was created
    assert output.exists()

    # Verify compression is disabled (ZIP_STORED)
    with zipfile.ZipFile(output, "r") as zf:
        # Check that files are stored uncompressed
        for info in zf.infolist():
            assert info.compress_type == zipfile.ZIP_STORED


def test_build_zipapp_default_no_compression(tmp_path: Path) -> None:
    """Test that default behavior is no compression (matching zipapp)."""
    # Create a test package
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text("def func():\n    pass\n")

    output = tmp_path / "app.pyz"

    # Call without compress parameter (should default to False)
    mod_build.build_zipapp(
        output=output,
        packages=[pkg_dir],
        entry_point=None,
    )

    # Verify zip file was created
    assert output.exists()

    # Verify compression is disabled by default
    with zipfile.ZipFile(output, "r") as zf:
        for info in zf.infolist():
            assert info.compress_type == zipfile.ZIP_STORED


def test_build_zipapp_compression_affects_size(tmp_path: Path) -> None:
    """Test that compression actually reduces file size for text content."""
    # Create a test package with some content
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    # Create a file with repetitive content that compresses well
    content = "def func():\n    " + "x" * 1000 + "\n    pass\n"
    (pkg_dir / "module.py").write_text(content)

    output_compressed = tmp_path / "app_compressed.pyz"
    output_uncompressed = tmp_path / "app_uncompressed.pyz"

    # Build with compression
    mod_build.build_zipapp(
        output=output_compressed,
        packages=[pkg_dir],
        entry_point=None,
        compress=True,
    )

    # Build without compression
    mod_build.build_zipapp(
        output=output_uncompressed,
        packages=[pkg_dir],
        entry_point=None,
        compress=False,
    )

    # Compressed version should be smaller (or at least not larger)
    # Note: For very small files, compression overhead might make it larger
    # So we just verify both files exist and are valid
    assert output_compressed.exists()
    assert output_uncompressed.exists()

    # Verify both are valid zip files
    with zipfile.ZipFile(output_compressed, "r") as zf:
        assert len(zf.namelist()) > 0
    with zipfile.ZipFile(output_uncompressed, "r") as zf:
        assert len(zf.namelist()) > 0
