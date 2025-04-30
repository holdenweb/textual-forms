import wingdbstub
import pytest

import tempfile

from setver import update_project_version, read_version, write_version, TomlProcessingError, VersionValidationError

# Create a dummy pyproject.toml for testing

def content(version):
    toml_part1 = """
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
description = "A sample package"
"""
    toml_part2 = """
readme = "README.md"
requires-python = ">=3.8"
"Bug Tracker" = "https://github.com/pypa/sampleproject/issues"
    """
    version = f"version = '{version}'\n" if version else ""
    return f"{toml_part1}\n{version}{toml_part2}"

def temp_toml():
    return tempfile.NamedTemporaryFile(
        mode="w",
        buffering=-1,
        encoding="utf-8",
        suffix=".toml",
        prefix="pyproject-",
        delete=True,
        delete_on_close=False,
    )

def attempt_update(f, version, exception):
    with pytest.raises(exception):
        update_project_version(f.name, version)

def version_format_invalid(testfile):
    with pytest.raises(expected_exception):
        pass

def missing_version(testfile2):
    pass

def missing_toml_file():
    pass

@pytest.mark.parametrize("version,exception", [
    ('0.9.0', VersionValidationError),
    ('invalid-version', VersionValidationError),

])
def test_exception_raising(version, exception):
    with temp_toml() as f:
        f.write(content(version))
        f.close()
        attempt_update(f, version, exception)
