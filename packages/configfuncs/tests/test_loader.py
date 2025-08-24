from configfuncs.loader import load_config, resolve_callable

def test_load_config_has_entries():
    cfg = load_config()
    assert "Multiply" in cfg and "Echo" in cfg


def test_resolve_callable_multiply():
    cfg = load_config()
    entry = cfg["Multiply"]
    cls = resolve_callable(entry)
    # avoid importing elementals here; just check callable name
    assert cls.__name__ == "MultiplyFunction"
