from pathlib import Path
import subprocess
import shutil
import pkginfo

testing_assets = Path(__file__).parent / "assets"
plugin_source_dir = Path(__file__).parent.parent / "poetry_version_plugin"


def test_defaults(tmp_path: Path):
    no_packages_path = testing_assets / "no_packages"
    testing_dir = tmp_path / "testing_package"
    shutil.copytree(no_packages_path, testing_dir)
    result = subprocess.run(
        [
            "coverage",
            "run",
            "--source",
            str(plugin_source_dir),
            "--parallel-mode",
            "-m",
            "poetry",
            "build",
        ],
        cwd=testing_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert (
        "Using __init__.py file at test_custom_version/__init__.py for dynamic version"
        in result.stdout
    )
    assert (
        "Setting package dynamic version to __version__ variable from __init__.py: 0.0.1"
        in result.stdout
    )
    assert "Built test_custom_version-0.0.1-py3-none-any.whl" in result.stdout
    wheel_path = testing_dir / "dist" / "test_custom_version-0.0.1-py3-none-any.whl"
    info = pkginfo.get_metadata(str(wheel_path))
    assert info.version == "0.0.1"
    coverage_path = list(testing_dir.glob(".coverage*"))[0]
    dst_coverage_path = Path(__file__).parent.parent / coverage_path.name
    dst_coverage_path.write_bytes(coverage_path.read_bytes())


def test_custom_packages(tmp_path: Path):
    package_path = testing_assets / "custom_packages"
    testing_dir = tmp_path / "testing_package"
    shutil.copytree(package_path, testing_dir)
    result = subprocess.run(
        [
            "coverage",
            "run",
            "--source",
            str(plugin_source_dir),
            "--parallel-mode",
            "-m",
            "poetry",
            "build",
        ],
        cwd=testing_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert (
        "Using __init__.py file at custom_package/__init__.py for dynamic version"
        in result.stdout
    )
    assert (
        "Setting package dynamic version to __version__ variable from __init__.py: 0.0.2"
        in result.stdout
    )
    assert "Built test_custom_version-0.0.2-py3-none-any.whl" in result.stdout
    wheel_path = testing_dir / "dist" / "test_custom_version-0.0.2-py3-none-any.whl"
    info = pkginfo.get_metadata(str(wheel_path))
    assert info.version == "0.0.2"
    coverage_path = list(testing_dir.glob(".coverage*"))[0]
    dst_coverage_path = Path(__file__).parent.parent / coverage_path.name
    dst_coverage_path.write_bytes(coverage_path.read_bytes())


def test_variations(tmp_path: Path):
    package_path = testing_assets / "variations"
    testing_dir = tmp_path / "testing_package"
    shutil.copytree(package_path, testing_dir)
    result = subprocess.run(
        [
            "coverage",
            "run",
            "--source",
            str(plugin_source_dir),
            "--parallel-mode",
            "-m",
            "poetry",
            "build",
        ],
        cwd=testing_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert (
        "Using __init__.py file at test_custom_version/__init__.py for dynamic version"
        in result.stdout
    )
    assert (
        "Setting package dynamic version to __version__ variable from __init__.py: 0.0.3"
        in result.stdout
    )
    assert "Built test_custom_version-0.0.3-py3-none-any.whl" in result.stdout
    wheel_path = testing_dir / "dist" / "test_custom_version-0.0.3-py3-none-any.whl"
    info = pkginfo.get_metadata(str(wheel_path))
    assert info.version == "0.0.3"
    coverage_path = list(testing_dir.glob(".coverage*"))[0]
    dst_coverage_path = Path(__file__).parent.parent / coverage_path.name
    dst_coverage_path.write_bytes(coverage_path.read_bytes())
