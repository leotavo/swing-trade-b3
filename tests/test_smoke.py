import importlib


def test_import_app():
    mod = importlib.import_module("app")
    assert mod is not None


def test_version_available():
    import app

    assert isinstance(app.__version__, str)
    assert app.__version__


def test_main_returns_zero():
    from app.__main__ import main

    assert main() == 0
