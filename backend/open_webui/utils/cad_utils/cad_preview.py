"""
@author 30hours
"""

import re
import cadquery as cq
from cadquery.vis import Showable
from typing import Tuple, Optional
from .CadQueryValidator import CadQueryValidator
from .Preview import preview


def dummy_func(*args, **kwargs):
    return


def execute_code(code: str) -> Tuple[Optional[Showable], Optional[str]]:
    namespace = {"cq": {"exporters": {"export": dummy_func}}, "show_object": dummy_func, "print": dummy_func}
    try:
        exec(code, namespace)
    except Exception as e:
        return None, str(e)

    result = parse_result_variable(code, namespace)
    if result is None:
        return None, "parse result failed"
    else:
        return result, None


def parse_result_variable(code: str, namespace: dict) -> Showable | None:
    result = namespace.get("result", None)
    if result:
        return result

    reg_list = [r"exporters\.export\((.+),", r"(\w+)\.save\("]
    for reg in reg_list:
        m = re.search(reg, code)
        if m:
            result = m.group(1).strip()
            result = namespace.get(result, None)
            if result:
                return result
    return None


def execute_and_preview(code: str) -> Tuple[Optional[dict], Optional[str]]:
    clean_code, error = CadQueryValidator().validate(code)
    if error:
        return None, error

    assert clean_code
    result = execute_code(clean_code)
    return preview(result)
