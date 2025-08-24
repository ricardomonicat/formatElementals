from elementals.examples.echo import EchoFunction
from elementals.params import ElementalParams

def test_echo_roundtrip():
    fn = EchoFunction()
    params = ElementalParams(params={"a": 1}, savepoint={"step": "x"})
    resp = fn.run(params)
    assert resp["status"] == "success"
    assert resp["data"]["echo"] == {"a": 1}
    assert resp["data"]["savepoint"] == {"step": "x"}
