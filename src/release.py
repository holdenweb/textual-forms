import sys
import subprocess
from glob import glob

from setver import read_version, update_project_version, VersionValidationError

VERSION_TEMPLATE = """\

__version__ = "{version}"

"""

def release(version):
    # Ensure a clean environment
    if subprocess.call("git diff --quiet".split()) != 0:
        sys.exit("Current git branch is dirty: please commit "
                 "or stash changes before releasing")

    # Ensure no debug calls remain!
    oopsies = []
    stubs = list(glob("**/wingdbstub.py", recursive=True))
    for source in glob("**/*.py", recursive=True):
        if source in stubs:
            continue
        # TODO: fix release process to omit wingdbstub file(s)
        with open(source) as f:
            if ("import" + " wingdbstub") in f.read():
                oopsies.append(source)
    if oopsies:
        sys.exit(f"Some files still import wingdbstub: {oopsies!r}")

    # We are clear to update the version - if it passes validation
    try:
        update_project_version('pyproject.toml', version)
    except VersionValidationError as e:
        sys.exit(e)

    # Check in an updated version.py
    pystring = VERSION_TEMPLATE.format(version=version)
    with open("src/textual_forms/version.py", "w") as pyfile:
        pyfile.write(pystring)
        print("Wrote", pyfile)
    retcode = subprocess.call(["uv", "lock"])
    cmd = ["git", "add", "uv.lock", "pyproject.toml", "src/textual_forms/version.py"]  # Note: excludes files previously added
    retcode = subprocess.call(cmd)
    cmd = ["git", "commit", "-m", f"Release r{version}"]
    retcode = subprocess.call(cmd)

    # Tag the new version
    cmd = ["git", "tag", f"r{version}"]
    retcode = subprocess.call(cmd)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(read_version("pyproject.toml"))
        sys.exit()

    elif len(sys.argv) != 2:
        sys.exit(usage())

    else:
        release(sys.argv[1])
