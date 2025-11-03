"""Nox sessions."""

import sys
from pathlib import Path
from textwrap import dedent

import nox

package = "skimpy"
python_versions = ["3.12", "3.11", "3.10"]
nox.needs_version = ">= 2021.6.6"
nox.options.default_venv_backend = "uv"
nox.options.sessions = (
    "pre-commit",
    # "mypy",
    "tests",
    "typeguard",
    "xdoctest",
)


def activate_virtualenv_in_precommit_hooks(session: nox.Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.
    """
    if session.bin is None:
        return

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        text = hook.read_text()
        bindir = repr(session.bin)[1:-1]  # strip quotes
        if not (
            Path("A") == Path("a") and bindir.lower() in text.lower() or bindir in text
        ):
            continue

        lines = text.splitlines()
        if not (lines[0].startswith("#!") and "python" in lines[0].lower()):
            continue

        header = dedent(
            f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """
        )

        lines.insert(1, header)
        hook.write_text("\n".join(lines))


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.run_install(
        "uv",
        "sync",
        "--group",
        "dev",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.env["PYTHONPATH"] = "src"

    try:
        session.run(
            "coverage",
            "run",
            "--parallel",
            "-m",
            "pytest",
            "--cache-clear",
            external=True,
            env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
            *session.posargs,
        )
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@nox.session(python=python_versions[0])
def coverage(session: nox.Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]
    session.run(
        "uv",
        "pip",
        "install",
        "coverage[toml]",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
        external=True,
    )
    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "erase", "--data-file=.coverage")
        session.run("coverage", "combine")

    session.run("coverage", *args, "-i")


@nox.session(name="pre-commit", python="3.10", venv_backend="uv")
def precommit(session: nox.Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.run_install(
        "uv",
        "sync",
        "--extra=dev",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@nox.session(python=python_versions, venv_backend="uv")
def mypy(session: nox.Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["src"]  # TODO reintroduce the tests folder here

    # Install project and dependencies using uv
    session.run_install(
        "uv",
        "sync",
        "--extra=dev",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run_install("uv", "pip", "install", "-e", ".")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@nox.session(venv_backend="uv", python=python_versions)
def typeguard(session: nox.Session) -> None:
    """Runtime type checking using Typeguard."""
    # Install project and dependencies using uv
    session.run_install(
        "uv",
        "sync",
        "--extra=dev",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run_install("uv", "pip", "install", "-e", ".")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@nox.session(venv_backend="uv", python=python_versions)
def xdoctest(session: nox.Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]

    # Install project and dependencies using uv
    session.run_install(
        "uv",
        "sync",
        "--extra=dev",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run_install("uv", "pip", "install", "-e", ".")
    session.run("python", "-m", "xdoctest", package, *args)
