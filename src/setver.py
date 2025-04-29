import toml
import semver
import sys
import os
from typing import Dict, Any

# Define custom exception classes for clarity (optional but good practice)
class VersionValidationError(Exception):
    """Custom exception for version validation errors."""
    pass

class TomlProcessingError(Exception):
    """Custom exception for TOML file processing errors."""
    pass

def update_project_version(toml_file_path: str, new_version_str: str) -> None:
    """
    Updates the 'project.version' in a TOML file if the new version is valid
    and greater than the existing version.

    Args:
        toml_file_path: The path to the TOML file (e.g., 'pyproject.toml').
        new_version_str: The new version string to set (e.g., '1.2.3').

    Raises:
        FileNotFoundError: If the TOML file does not exist.
        TomlProcessingError: If the TOML file is invalid or missing expected keys.
        VersionValidationError: If the new or existing version string is not
                                 a valid semantic version, or if the new version
                                 is not strictly greater than the existing one.

    Side Effects:
        - Prints status messages to standard output.
        - Modifies the specified TOML file if validation passes.
        - Exits the program via sys.exit(1) if validation fails as requested.
          (Note: In library code, raising exceptions is often preferred over exiting,
           but adhering to the prompt's requirement here.)
    """
    #print(f"--- Starting version update for: {toml_file_path} ---")
    #print(f"Attempting to set version to: {new_version_str}")

    # 1. Validate the new version string format using semver
    try:
        new_version = semver.Version.parse(new_version_str)
        #print(f"New version '{new_version_str}' is valid semver.")
    except ValueError:
        # Use f-string for cleaner formatting
        error_message = (
            f"Error: Provided new version '{new_version_str}' is not a "
            f"valid semantic version (e.g., '1.2.3', '2.0.0-rc.1')."
        )
        raise  VersionValidationError(error_message)

    # 2. Read the TOML file
    if not os.path.exists(toml_file_path):
        raise OSError(f"Error: TOML file not found at '{toml_file_path}'.", file=sys.stderr)

    try:
        with open(toml_file_path, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = toml.load(f)
        #print(f"Successfully read TOML file: {toml_file_path}")
    except toml.TomlDecodeError as e:
        error_message = (f"Error: Failed to decode TOML file '{toml_file_path}'. Invalid syntax."
                         f"Details: {e}")
        raise ValueError(error_message)
    except IOError as e:
        raise OSError(f"Error: Could not read file '{toml_file_path}'. "
              f"Details: {e}")

    # 3. Validate the structure and get the existing version
    try:
        existing_version_str = data['project']['version']
        #print(f"Found existing version: {existing_version_str}")
    except KeyError:
        error_message = (
            f"Error: Could not find 'project.version' key in "
            f"'{toml_file_path}'. Ensure the file follows the "
            f"PEP 621 standard structure (or has [project][version])."
        )
        raise ValueError(error_message)
    except TypeError:
        error_message = (
           f"Error: The structure under 'project' in '{toml_file_path}' "
           f"is not a table/dictionary as expected."
        )
        raise TypeError(error_message)


    # 4. Validate the existing version string format
    try:
        existing_version = semver.Version.parse(existing_version_str)
        #print(f"Existing version '{existing_version_str}' is valid semver.")
    except ValueError:
        error_message = (
            f"Error: Existing version '{existing_version_str}' in "
            f"'{toml_file_path}' is not a valid semantic version."
        )
        raise ValueError(error_message, file=sys.stderr)

    # 5. Compare the versions
    if new_version <= existing_version:
        error_message = (
            f"Error: New version '{new_version_str}' is not strictly greater "
            f"than the existing version '{existing_version_str}'."
        )
        raise ValuError(error_messager)

    # 6. Update the data dictionary
    data['project']['version'] = new_version_str

    # 7. Write the updated data back to the TOML file
    try:
        with open(toml_file_path, 'w', encoding='utf-8') as f:
            toml.dump(data, f)
        #print(f"Successfully updated '{toml_file_path}' to version '{new_version_str}'.")
    except IOError as e:
        raise IOError(f"Error: Could not write updated file '{toml_file_path}'. "
                      f"Details: {e}", file=sys.stderr)

    #print(f"--- Version update complete for: {toml_file_path} ---")

# --- Example Usage ---
if __name__ == "__main__":
    # Create a dummy pyproject.toml for testing
    dummy_toml_content = """
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my_package"
version = "0.1.0" # <--- The version to be updated
description = "A sample package"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/pypa/sampleproject"
"Bug Tracker" = "https://github.com/pypa/sampleproject/issues"
"""
    dummy_file = "pyproject_test.toml"
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write(dummy_toml_content)

    print(f"Created dummy file: {dummy_file}")
    print("-" * 20)

    # --- Test Cases ---

    # Test Case 1: Successful update
    print("\nTest Case 1: Successful update")
    try:
        update_project_version(dummy_file, "0.2.0")
        # Verify content (optional)
        with open(dummy_file, "r") as f:
            print(f"\nContent of {dummy_file} after update:\n{f.read()}")
    except SystemExit as e:
        print(f"Test Case 1 exited with code: {e.code}") # Should not happen here
    print("-" * 20)

    # Test Case 2: New version not greater
    print("\nTest Case 2: New version not greater")
    try:
        update_project_version(dummy_file, "0.1.5") # 0.1.5 <= 0.2.0
    except SystemExit as e:
        print(f"Test Case 2 correctly exited with code: {e.code}") # Expected exit(1)
    print("-" * 20)

    # Test Case 3: Invalid new version format
    print("\nTest Case 3: Invalid new version format")
    try:
        update_project_version(dummy_file, "invalid-version")
    except SystemExit as e:
        print(f"Test Case 3 correctly exited with code: {e.code}") # Expected exit(1)
    print("-" * 20)

     # Test Case 4: File not found
    print("\nTest Case 4: File not found")
    try:
        update_project_version("non_existent_file.toml", "1.0.0")
    except SystemExit as e:
        print(f"Test Case 4 correctly exited with code: {e.code}") # Expected exit(1)
    print("-" * 20)

    # Test Case 5: Missing project.version key (Modify the file first)
    print("\nTest Case 5: Missing project.version")
    with open(dummy_file, "w", encoding="utf-8") as f:
         f.write("[project]\nname = 'test'") # Write incomplete TOML
    try:
        update_project_version(dummy_file, "1.0.0")
    except SystemExit as e:
        print(f"Test Case 5 correctly exited with code: {e.code}") # Expected exit(1)
    print("-" * 20)


    # Clean up the dummy file
    # os.remove(dummy_file)
    # print(f"\nCleaned up dummy file: {dummy_file}")