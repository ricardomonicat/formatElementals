from configfuncs.loader import get_function_instance, run_function
from elementals.params import ElementalParams


def test_run_multiply_via_yaml_instance():
    fn = get_function_instance("Multiply")
    out = fn.run(ElementalParams(params={"a": 2, "b": 5}))
    assert out["status"] == "success"
    assert out["data"]["product"] == 10


def test_run_multiply_via_yaml_helper():
    out = run_function("Multiply", params={"a": 2, "b": 5})
    assert out["status"] == "success"
    assert out["data"]["product"] == 10
