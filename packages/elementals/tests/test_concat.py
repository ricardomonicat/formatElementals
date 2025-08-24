from elementals.examples.concat import ConcatFunction
from elementals.params import ElementalParams

def test_concat_success():
    fn = ConcatFunction()
    params = ElementalParams(params={"text1": "Hello", "text2": "World"})
    resp = fn.run(params)
    assert resp["status"] == "success"
    assert resp["data"]["text1"] == "Hello"
    assert resp["data"]["text2"] == "World"
    assert resp["data"]["concat"] == "HelloWorld"


def test_concat_missing_param():
    fn = ConcatFunction()
    params = ElementalParams(params={"text1": "Hello"})
    resp = fn.run(params)
    assert resp["status"] == "error"
    assert resp["error"]["code"] == "missing_param"
