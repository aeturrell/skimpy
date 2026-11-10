"""Check that every place listing supported Python versions agrees.

The single source of truth is ``requires-python`` in pyproject.toml. This
check fails if ``.python-version``, the trove classifiers, or the nox
``python_versions`` list drift away from it.
"""

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("."))


def main() -> int:
    """Run the consistency checks and report any problems.

    Returns:
        int: 0 if all versions agree, 1 otherwise.
    """
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    requires = pyproject["project"]["requires-python"]
    match = re.fullmatch(r">=\s*(\d+\.\d+)", requires.strip())
    if not match:
        print(f"Unsupported requires-python format: {requires!r}")
        return 1
    minimum = _version_tuple(match.group(1))

    classifiers = {
        c.rsplit("::", 1)[1].strip()
        for c in pyproject["project"]["classifiers"]
        if re.fullmatch(r"Programming Language :: Python :: \d+\.\d+", c)
    }
    noxfile = (ROOT / "noxfile.py").read_text()
    nox_match = re.search(r"^python_versions = \[(.*?)\]", noxfile, re.MULTILINE)
    nox_versions = (
        set(re.findall(r"\"(\d+\.\d+)\"", nox_match.group(1))) if nox_match else set()
    )
    pinned = (ROOT / ".python-version").read_text().strip()

    errors = []
    if _version_tuple(pinned) < minimum:
        errors.append(
            f".python-version ({pinned}) is below requires-python ({requires})"
        )
    if pinned not in nox_versions:
        errors.append(
            f".python-version ({pinned}) is not tested in noxfile.py {sorted(nox_versions)}"
        )
    if classifiers != nox_versions:
        errors.append(
            f"Classifiers {sorted(classifiers)} differ from noxfile.py {sorted(nox_versions)}"
        )
    if min(nox_versions, key=_version_tuple, default=None) != match.group(1):
        errors.append(
            f"Lowest nox version should equal requires-python minimum ({match.group(1)})"
        )

    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
