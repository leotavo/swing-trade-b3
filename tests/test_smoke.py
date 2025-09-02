import importlib


def test_import_app():
    mod = importlib.import_module("app")
    # Avoid identity check warning; assert a meaningful property instead
    assert getattr(mod, "__name__", None) == "app"


def test_version_available():
    import app

    assert isinstance(app.__version__, str)
    assert app.__version__


def test_main_returns_zero():
    from app.__main__ import main

    assert main() == 0
