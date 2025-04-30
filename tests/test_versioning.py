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

def attempt_update(filename, version, exception):
    with pytest.raises(exception):
        update_project_version(filename, version if version else "2.3.4")

@pytest.mark.parametrize("version,exception", [
    ('0.9.0', VersionValidationError),
    ('not-a-vsn', VersionValidationError),
    (None, TomlProcessingError)
])
def test_exceptions(version, exception):
    with temp_toml() as f:
        f.write(content(version))
        f.close()
        attempt_update(f.name, version, exception)

def test_no_file():
    attempt_update("no_such_file", "9.9.9", IOError)

def test_version_present():
    import textual_forms
    assert hasattr(textual_forms, '__version__')