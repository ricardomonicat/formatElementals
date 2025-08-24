from elementals.utils.pathmap import resolve_path, render_template
from elementals.params import ElementalParams


def test_resolve_simple_and_index():
    ep = ElementalParams(params={"a": 1, "items": [
        {"id": 10}, {"id": 20}
    ]}, savepoint={"step": "x"}, meta={"config": {"ts": 123}})

    assert resolve_path(ep, "$params.a") == 1
    assert resolve_path(ep, "params.items[1].id") == 20
    assert resolve_path(ep, "savepoint.step") == "x"
    assert resolve_path(ep, "meta.config.ts") == 123
    assert resolve_path(ep, "params.missing") is None


def test_render_template_nested():
    ep = ElementalParams(params={"user": {"id": 7, "name": "Ada"}, "items": [10, 11]}, savepoint={})

    tpl = {
        "uid": "$params.user.id",
        "first": "$params.user.name",
        "order": {"items": ["$params.items[0]", "$params.items[1]"]},
        "static": 42,
    }
    out = render_template(ep, tpl)
    assert out == {"uid": 7, "first": "Ada", "order": {"items": [10, 11]}, "static": 42}
