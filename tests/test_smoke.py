import importlib


def test_import_app():
    mod = importlib.import_module("swing_trade_b3")
    # Avoid identity check warning; assert a meaningful property instead
    assert getattr(mod, "__name__", None) == "swing_trade_b3"


def test_version_available():
    import swing_trade_b3 as app

    assert isinstance(app.__version__, str)
    assert app.__version__


def test_main_returns_zero():
    from swing_trade_b3.__main__ import main

    assert main() == 0
