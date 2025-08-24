from typing import Any, Dict

import pytest

from elementals.params import ElementalParams, ProcessInfo, Environment, Meta
from elementals.utils.param_paths import resolve_path, resolve_template, apply_path_map


def sample_params() -> ElementalParams:
    return ElementalParams(
        params={
            "a": 2,
            "b": 5,
            "items": [
                {"val": 10},
                {"val": 20},
            ],
        },
        savepoint={"last": {"product": 40}},
        process=ProcessInfo(process_id="proc-123", version=2, run_id="run-9"),
        environment=Environment(name="qa", debug=True, region="eu", max_retries=3),
        meta=Meta(call_id="cid-1"),
    )


def test_resolve_path_basic():
    p = sample_params()
    assert resolve_path(p, "$params.a") == 2
    assert resolve_path(p, "$params.items[1].val") == 20
    assert resolve_path(p, "$savepoint.last.product") == 40
    assert resolve_path(p, "$process.process_id") == "proc-123"


def test_resolve_missing_modes():
    p = sample_params()
    # default None
    assert resolve_template({"x": "$params.nope"}, p) == {"x": None}
    # keep
    assert resolve_template({"x": "$params.nope"}, p, on_missing="keep") == {"x": "$params.nope"}
    # error
    with pytest.raises(KeyError):
        resolve_template({"x": "$params.nope"}, p, on_missing="error")


def test_resolve_template_nested_and_tuple():
    p = sample_params()
    tpl = {
        "product": "$savepoint.last.product",
        "inputs": {"a": "$params.a", "b": "$params.b"},
        "pair": ("static", "$process.run_id"),
        "list": ["$params.items[0].val", "$params.items[1].val"],
    }
    out = resolve_template(tpl, p)
    assert out == {
        "product": 40,
        "inputs": {"a": 2, "b": 5},
        "pair": ("static", "run-9"),
        "list": [10, 20],
    }


def test_apply_path_map_alias():
    p = sample_params()
    path_map = {
        "sum": "$params.a",
        "env": "$environment",
    }
    out = apply_path_map(path_map, p)
    assert out["sum"] == 2
    # environment is a model, should be dumped to dict
    assert isinstance(out["env"], dict)
    assert out["env"]["name"] == "qa"
