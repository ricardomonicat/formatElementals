from elementals.params import ElementalParams
from elementals.examples.lcm import LCMFunction

def test_lcm_success():
    fn = LCMFunction()
    out = fn.run(ElementalParams(params={"a": 6, "b": 8}))
    assert out["status"] == "success"
    assert out["data"]["lcm"] == 24

def test_lcm_missing_param():
    fn = LCMFunction()
    out = fn.run(ElementalParams(params={"a": 6}))
    assert out["status"] == "error"
    assert out["error"]["code"] == "missing_param"
