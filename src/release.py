import sys
import subprocess

from setver import read_version, update_project_version

VERSION_TEMPLATE = """\

__version__ = "{version}"

"""

def release(version):
    # Modify version according to argument
    if subprocess.call("git diff --quiet".split()) != 0:
        sys.exit("Current git branch is dirty: please commit "
                 "or stash changes before releasing")
    update_project_version('pyproject.toml', version)

    # Check in an updated version.py
    pystring = VERSION_TEMPLATE.format(version=version)
    with open("src/textual_forms/version.py", "w") as pyfile:
        pyfile.write(pystring)
        print("Wrote", pyfile)
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
