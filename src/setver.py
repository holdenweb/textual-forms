import toml
import semver
import os
import sys
from typing import Dict, Any

# --- Custom Exception Classes ---
class VersionValidationError(ValueError): # Inherit from ValueError for type context
    """Custom exception for semantic version validation errors."""
    pass

class TomlProcessingError(Exception):
    """Custom exception for TOML file processing errors (structure, keys)."""
    pass

# --- Core Functions ---

def read_version(toml_file_path: str) -> str:
    """
    Reads the TOML file and returns the value of 'project.version'.

    Args:
        toml_file_path: The path to the TOML file.

    Returns:
        The version string found in 'project.version'.

    Raises:
        FileNotFoundError: If the TOML file does not exist.
        TomlProcessingError: If the TOML file is invalid, missing 'project'
                             or 'project.version' keys, or if 'project'
                             is not a table/dictionary.
        IOError: If there's an error reading the file.
    """
    if not os.path.exists(toml_file_path):
        raise FileNotFoundError(f"TOML file not found at '{toml_file_path}'.")

    try:
        with open(toml_file_path, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = toml.load(f)
    except toml.TomlDecodeError as e:
        raise TomlProcessingError(
            f"Failed to decode TOML file '{toml_file_path}'. Invalid syntax. Details: {e}"
            ) from e
    except IOError as e:
        # Catching base IOError, could be permission error etc.
        raise IOError(f"Could not read file '{toml_file_path}'. Details: {e}") from e

    try:
        project_table = data['project']
        if not isinstance(project_table, dict):
            raise TomlProcessingError(
                 f"The 'project' key in '{toml_file_path}' is not a table/dictionary."
             )
        existing_version_str = project_table['version']
        return existing_version_str
    except KeyError as e:
        raise TomlProcessingError(
            f"Could not find key '{e}' within 'project' section in '{toml_file_path}'. "
            "Ensure '[project]' table and 'version' key exist."
            ) from e
    except TypeError:
        # This might occur if 'project' exists but isn't subscriptable (e.g., project = true)
        raise TomlProcessingError(
             f"Expected 'project' to be a table/dictionary in '{toml_file_path}', but found {type(data.get('project'))}."
         )


def write_version(toml_file_path: str, new_version_str: str) -> None:
    """
    Reads the TOML file, updates 'project.version', and writes it back.

    Args:
        toml_file_path: The path to the TOML file.
        new_version_str: The new version string to write.

    Raises:
        FileNotFoundError: If the TOML file does not exist (during read phase).
        TomlProcessingError: If the TOML file is invalid or 'project' is not a table.
        IOError: If there's an error reading or writing the file.
        TypeError: If 'project' exists but isn't a dictionary during read.
        KeyError: If 'project' key doesn't exist during read.
    """
    # Read the data first to preserve other contents
    try:
        if not os.path.exists(toml_file_path):
                # Raise specific error although read_version might have caught it if called first
            raise FileNotFoundError(f"TOML file not found at '{toml_file_path}' for writing.")

        with open(toml_file_path, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = toml.load(f)

        # Ensure project table exists and is a table before modifying
        if 'project' not in data:
            raise TomlProcessingError(f"Missing 'project' table in '{toml_file_path}'. Cannot update version.")
        if not isinstance(data['project'], dict):
            raise TomlProcessingError(f"'project' key in '{toml_file_path}' is not a table/dictionary. Cannot update version.")

        # Update the version
        data['project']['version'] = new_version_str

    except toml.TomlDecodeError as e:
        raise TomlProcessingError(
             f"Failed to decode TOML file '{toml_file_path}' before writing. Invalid syntax. Details: {e}"
            ) from e
    except (IOError, KeyError, TypeError) as e: # Catch read-related errors
        if isinstance(e, IOError):
            raise IOError(f"Could not read file '{toml_file_path}' before writing. Details: {e}") from e
        else:
            raise TomlProcessingError(f"Error preparing file '{toml_file_path}' for writing: {e}") from e


    # Write the updated data back
    try:
        with open(toml_file_path, 'w', encoding='utf-8') as f:
            toml.dump(data, f)
    except IOError as e:
        raise IOError(f"Could not write updated file '{toml_file_path}'. Details: {e}") from e


def update_project_version(toml_file_path: str, new_version_str: str) -> None:
    """
    Orchestrates updating the 'project.version' in a TOML file if the
    new version is valid and greater than the existing version.

    Args:
        toml_file_path: The path to the TOML file (e.g., 'pyproject.toml').
        new_version_str: The new version string to set (e.g., '1.2.3').

    Raises:
        FileNotFoundError: If the TOML file does not exist.
        TomlProcessingError: If the TOML file is invalid or has structure issues.
        VersionValidationError: If the new or existing version string is not
                                a valid semantic version, or if the new version
                                is not strictly greater than the existing one.
        IOError: If file read/write errors occur.
        TypeError: If TOML structure is incorrect.
        KeyError: If expected TOML keys are missing.
    """
    # Validate the new version string format using semver
    try:
        new_version = semver.Version.parse(new_version_str)
    except ValueError:
        # Raise specific custom exception
        raise VersionValidationError(
            f"Provided new version '{new_version_str}' is not a valid semantic version (e.g., '1.2.3')."
        )

    # Read existing version (delegate error handling to read_version)
    # Exceptions from read_version (FileNotFound, TomlProcessingError, IOError) will propagate up
    existing_version_str = read_version(toml_file_path)

    # Validate the existing version string format
    try:
        existing_version = semver.Version.parse(existing_version_str)
    except ValueError:
        raise VersionValidationError(
            f"Existing version '{existing_version_str}' in '{toml_file_path}' is not a valid semantic version."
        )
    # Compare the versions
    if new_version <= existing_version:
        raise VersionValidationError(
            f"New version '{new_version_str}' ({new_version}) is not strictly greater "
            f"than the existing version '{existing_version_str}' ({existing_version})."
        )

    # Write the new version (delegate error handling to write_version)
    # Exceptions from write_version will propagate up
    write_version(toml_file_path, new_version_str)

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            print(read_version('pyproject.toml'))
        elif len(sys.argv) == 2:
            update_project_version('pyproject.toml', sys.argv[1])
        else:
            sys.exit("Aborted: additional arguments detected")
    except Exception as e:
        sys.exit(f"Oops: {e}")