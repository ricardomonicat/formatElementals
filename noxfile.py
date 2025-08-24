import nox

PY_VERS = ["3.10", "3.11", "3.12"]

@nox.session(python=PY_VERS)
def tests(session):
    session.install("-r", "requirements-dev.txt")
    session.install("-e", "packages/actionformats[dev]")
    session.install("-e", "packages/elementals[dev]")
    session.run("pytest", "-q")

@nox.session
def lint(session):
    session.install("ruff>=0.6", "black>=24.4")
    session.run("ruff", "check", "packages")
    session.run("black", "--check", "packages")

@nox.session
def type(session):
    session.install("mypy>=1.10", "typing-extensions>=4.7")
    session.run("mypy", "packages")

@nox.session
def build_all(session):
    session.install("build>=1.2")
    session.run("python", "scripts/build_all.py")
