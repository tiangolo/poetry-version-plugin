from pathlib import Path
import subprocess
import ast
from typing import Optional

from cleo.io.io import IO

from poetry.plugins.plugin import Plugin
from poetry.utils.helpers import module_name
from poetry.poetry import Poetry


def get_poetry_version_source(poetry: Poetry, io: IO) -> Optional[str]:
    poetry_version_config: dict = poetry.pyproject.data.get("tool", {}).get(
        "poetry-version", {}
    )
    if not poetry_version_config:
        io.write_line(
            "No section <b>[tool.poetry-version]</b> found in pyproject.toml, "
            "not extracting dynamic version"
        )
        return None
    version_source = poetry_version_config.get("source")
    if not version_source:
        io.write_line(
            "No <b>source</b> configuration found in [tool.poetry-version] in "
            "pyproject.toml, not extracting dynamic version"
        )
    return version_source


class InitVersion(Plugin):
    def activate(self, poetry: Poetry, io: IO):
        version_source = get_poetry_version_source(poetry=poetry, io=io)
        if not version_source == "init":
            return
        packages = poetry.local_config.get("packages")
        if packages:
            if len(packages) == 1:
                package_name = packages[0]["include"]
            else:
                io.write_error_line(
                    "More than one package set, " "cannot extract dynamic version"
                )
                return
        else:
            package_name = module_name(poetry.package.name)
        init_path = Path(package_name) / "__init__.py"
        if not init_path.is_file():
            io.write_error_line(
                f"__init__.py file not found at {init_path}, "
                "cannot extract dynamic version"
            )
        else:
            io.write_line(f"Using __init__.py file at {init_path} for dynamic version")
        tree = ast.parse(init_path.read_text())
        for el in tree.body:
            if isinstance(el, ast.Assign):
                if len(el.targets) == 1:
                    target = el.targets[0]
                    if isinstance(target, ast.Name):
                        if target.id == "__version__":
                            value_node = el.value
                            if isinstance(value_node, ast.Constant):
                                version = value_node.value
                                io.write_line(
                                    "Setting package dynamic version to __version__ "
                                    f"variable from __init__.py: <b>{version}</b>"
                                )
                                poetry.package.set_version(version)
                                return
        message = (
            "No valid __version__ variable found in __init__.py, "
            "cannot extract dynamic version"
        )
        io.write_error_line(message)
        raise RuntimeError(message)


class GitTagVersion(Plugin):
    def activate(self, poetry: Poetry, io: IO):
        version_source = get_poetry_version_source(poetry=poetry, io=io)
        if not version_source == "git-tag":
            return
        result = subprocess.run(
            ["git", "describe", "--exact-match", "--tags", "HEAD"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if result.returncode == 0:
            tag = result.stdout.strip()
            io.write_line(f"Git tag found, setting dynamic version to: {tag}")
            poetry.package.set_version(tag)
            return
        else:
            message = "No Git tag found, not extracting dynamic version"
            io.write_error_line(message)
            raise RuntimeError(message)
