from elementals.examples.multiply import MultiplyFunction
from elementals.params import ElementalParams

def test_multiply_success():
    print("wwwwwwww") 
    fn = MultiplyFunction()
    params = ElementalParams(params={"a": 3, "b": 4})
    resp = fn.run(params)
    assert resp["status"] == "success"
    assert resp["data"]["a"] == 3
    assert resp["data"]["b"] == 4
    assert resp["data"]["product"] == 12

def test_multiply_missing_param():
    fn = MultiplyFunction()
    print("ssssssss") 
    params = ElementalParams(params={"a": 3})
    resp = fn.run(params)
    assert resp["status"] == "error"
    assert resp["error"]["code"] == "missing_param"

### run_dict no longer needed since run returns dicts; kept tests concise
