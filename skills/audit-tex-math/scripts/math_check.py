#!/usr/bin/env python3
"""Reusable deterministic checks for TeX math audits.

The numeric subcommands use only the Python standard library. The sympy subcommands are
optional and print a clear error if SymPy is unavailable.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import statistics
import sys
from dataclasses import dataclass
from typing import Any


SAFE_FUNCS: dict[str, Any] = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_") and callable(getattr(math, name))
}
SAFE_FUNCS.update({"abs": abs, "max": max, "min": min, "pow": pow})
SAFE_CONSTS = {"pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf}

ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.USub,
    ast.UAdd,
)


@dataclass
class CheckResult:
    status: str
    payload: dict[str, Any]


def parse_values(raw: str | None) -> dict[str, float]:
    if not raw:
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("--values must be a JSON object")
    out: dict[str, float] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not key.isidentifier():
            raise ValueError(f"invalid variable name: {key!r}")
        if not isinstance(value, (int, float)):
            raise ValueError(f"value for {key!r} must be numeric")
        out[key] = float(value)
    return out


def parse_points(raw: str) -> list[dict[str, float]]:
    data = json.loads(raw)
    if isinstance(data, dict):
        return [parse_values(json.dumps(data))]
    if not isinstance(data, list):
        raise ValueError("--points must be a JSON object or list of objects")
    points: list[dict[str, float]] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("every point must be a JSON object")
        points.append(parse_values(json.dumps(item)))
    if not points:
        raise ValueError("--points must contain at least one point")
    return points


def parse_epsilons(raw: str) -> list[float]:
    data = json.loads(raw)
    if not isinstance(data, list) or len(data) < 2:
        raise ValueError("--epsilons must be a JSON list with at least two positive numbers")
    epsilons = []
    for value in data:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("all epsilon values must be positive numbers")
        epsilons.append(float(value))
    return epsilons


def validate_expr(expr: str, names: set[str]) -> ast.Expression:
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"disallowed expression syntax: {type(node).__name__}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in SAFE_FUNCS:
                raise ValueError("only whitelisted math function calls are allowed")
        if isinstance(node, ast.Name) and node.id not in names:
            raise ValueError(f"unknown name in expression: {node.id}")
    return tree


def eval_expr(expr: str, values: dict[str, float]) -> float:
    namespace = {**SAFE_FUNCS, **SAFE_CONSTS, **values}
    tree = validate_expr(expr, set(namespace))
    result = eval(compile(tree, "<math_check>", "eval"), {"__builtins__": {}}, namespace)
    if not isinstance(result, (int, float)):
        raise ValueError("expression did not evaluate to a scalar number")
    return float(result)


def numeric_eq(args: argparse.Namespace) -> CheckResult:
    values = parse_values(args.values)
    lhs = eval_expr(args.lhs, values)
    rhs = eval_expr(args.rhs, values)
    delta = lhs - rhs
    abs_delta = abs(delta)
    passed = abs_delta <= args.tolerance
    return CheckResult(
        "PASS" if passed else "FAIL",
        {
            "check": "numeric-eq",
            "lhs_expr": args.lhs,
            "rhs_expr": args.rhs,
            "values": values,
            "lhs_value": lhs,
            "rhs_value": rhs,
            "delta": delta,
            "abs_delta": abs_delta,
            "tolerance": args.tolerance,
        },
    )


def finite_diff(args: argparse.Namespace) -> CheckResult:
    values = parse_values(args.values)
    if args.var not in values:
        raise ValueError(f"--values must include differentiation variable {args.var!r}")
    h = args.h
    if h <= 0:
        raise ValueError("--h must be positive")
    x0 = values[args.var]
    plus_values = dict(values)
    minus_values = dict(values)
    plus_values[args.var] = x0 + h
    minus_values[args.var] = x0 - h
    approx = (eval_expr(args.expr, plus_values) - eval_expr(args.expr, minus_values)) / (2 * h)
    expected = eval_expr(args.expected, values)
    delta = approx - expected
    abs_delta = abs(delta)
    passed = abs_delta <= args.tolerance
    return CheckResult(
        "PASS" if passed else "FAIL",
        {
            "check": "finite-diff",
            "expr": args.expr,
            "var": args.var,
            "values": values,
            "h": h,
            "finite_difference": approx,
            "expected_expr": args.expected,
            "expected_value": expected,
            "delta": delta,
            "abs_delta": abs_delta,
            "tolerance": args.tolerance,
        },
    )


def grid_eq(args: argparse.Namespace) -> CheckResult:
    base_values = parse_values(args.values)
    points = parse_points(args.points)
    rows = []
    all_passed = True
    for idx, point in enumerate(points, start=1):
        values = {**base_values, **point}
        lhs = eval_expr(args.lhs, values)
        rhs = eval_expr(args.rhs, values)
        delta = lhs - rhs
        abs_delta = abs(delta)
        passed = abs_delta <= args.tolerance
        all_passed = all_passed and passed
        rows.append(
            {
                "point": idx,
                "values": values,
                "lhs_value": lhs,
                "rhs_value": rhs,
                "delta": delta,
                "abs_delta": abs_delta,
                "status": "PASS" if passed else "FAIL",
            }
        )
    return CheckResult(
        "PASS" if all_passed else "FAIL",
        {
            "check": "grid-eq",
            "lhs_expr": args.lhs,
            "rhs_expr": args.rhs,
            "points_checked": len(rows),
            "tolerance": args.tolerance,
            "rows": rows,
        },
    )


def residual_order(args: argparse.Namespace) -> CheckResult:
    base_values = parse_values(args.values)
    epsilons = parse_epsilons(args.epsilons)
    rows = []
    for eps in epsilons:
        values = dict(base_values)
        values[args.epsilon] = eps
        exact = eval_expr(args.exact, values)
        approx = eval_expr(args.approx, values)
        residual = abs(exact - approx)
        rows.append({"epsilon": eps, "exact": exact, "approx": approx, "residual": residual})

    pairwise_orders = []
    for left, right in zip(rows, rows[1:]):
        if left["residual"] <= 0 or right["residual"] <= 0:
            continue
        eps_ratio = left["epsilon"] / right["epsilon"]
        res_ratio = left["residual"] / right["residual"]
        if eps_ratio <= 0 or eps_ratio == 1 or res_ratio <= 0:
            continue
        pairwise_orders.append(math.log(res_ratio) / math.log(eps_ratio))

    if not pairwise_orders:
        raise ValueError("could not estimate residual order from the supplied epsilon grid")

    median_order = statistics.median(pairwise_orders)
    expected_order = args.expected_order
    passed = True if expected_order is None else median_order >= expected_order - args.tolerance
    return CheckResult(
        "PASS" if passed else "FAIL",
        {
            "check": "residual-order",
            "exact_expr": args.exact,
            "approx_expr": args.approx,
            "epsilon": args.epsilon,
            "base_values": base_values,
            "rows": rows,
            "pairwise_orders": pairwise_orders,
            "estimated_order": median_order,
            "expected_order": expected_order,
            "tolerance": args.tolerance,
        },
    )


def self_test(args: argparse.Namespace) -> CheckResult:
    tests = []
    cases = [
        ("numeric-eq", argparse.Namespace(lhs="x**2 - 1", rhs="0", values='{"x": 1}', tolerance=1e-9)),
        (
            "finite-diff",
            argparse.Namespace(expr="log(x)", var="x", expected="1/x", values='{"x": 2}', h=1e-6, tolerance=1e-5),
        ),
        (
            "grid-eq",
            argparse.Namespace(lhs="x**2", rhs="y", points='[{"x": 2, "y": 4}, {"x": 3, "y": 9}]', values=None, tolerance=1e-9),
        ),
        (
            "residual-order",
            argparse.Namespace(
                exact="exp(eps)",
                approx="1 + eps",
                epsilon="eps",
                epsilons="[0.1, 0.05, 0.025, 0.0125]",
                values=None,
                expected_order=2.0,
                tolerance=0.15,
            ),
        ),
    ]
    funcs = {
        "numeric-eq": numeric_eq,
        "finite-diff": finite_diff,
        "grid-eq": grid_eq,
        "residual-order": residual_order,
    }
    all_passed = True
    for name, namespace in cases:
        result = funcs[name](namespace)
        all_passed = all_passed and result.status == "PASS"
        tests.append({"name": name, "status": result.status, "payload": result.payload})
    return CheckResult(
        "PASS" if all_passed else "FAIL",
        {"check": "self-test", "tests": tests},
    )


def load_sympy() -> Any:
    try:
        import sympy as sp  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise RuntimeError("SymPy is required for this subcommand but is not installed") from exc
    return sp


def sympy_symbols(sp: Any, raw: str | None) -> dict[str, Any]:
    names = [name.strip() for name in (raw or "").split(",") if name.strip()]
    symbols = {}
    for name in names:
        if not name.isidentifier():
            raise ValueError(f"invalid symbol name: {name!r}")
        symbols[name] = sp.symbols(name)
    return symbols


def sympy_eq(args: argparse.Namespace) -> CheckResult:
    sp = load_sympy()
    local_dict = sympy_symbols(sp, args.symbols)
    lhs = sp.sympify(args.lhs, locals=local_dict)
    rhs = sp.sympify(args.rhs, locals=local_dict)
    simplified = sp.simplify(lhs - rhs)
    passed = simplified == 0
    return CheckResult(
        "PASS" if passed else "FAIL",
        {
            "check": "sympy-eq",
            "lhs_expr": args.lhs,
            "rhs_expr": args.rhs,
            "symbols": sorted(local_dict),
            "simplified_difference": str(simplified),
        },
    )


def sympy_diff(args: argparse.Namespace) -> CheckResult:
    sp = load_sympy()
    local_dict = sympy_symbols(sp, args.symbols)
    if args.var not in local_dict:
        local_dict[args.var] = sp.symbols(args.var)
    expr = sp.sympify(args.expr, locals=local_dict)
    expected = sp.sympify(args.expected, locals=local_dict)
    computed = sp.diff(expr, local_dict[args.var])
    simplified = sp.simplify(computed - expected)
    passed = simplified == 0
    return CheckResult(
        "PASS" if passed else "FAIL",
        {
            "check": "sympy-diff",
            "expr": args.expr,
            "var": args.var,
            "expected_expr": args.expected,
            "computed_derivative": str(computed),
            "simplified_difference": str(simplified),
            "symbols": sorted(local_dict),
        },
    )


def sympy_limit(args: argparse.Namespace) -> CheckResult:
    sp = load_sympy()
    local_dict = sympy_symbols(sp, args.symbols)
    if args.var not in local_dict:
        local_dict[args.var] = sp.symbols(args.var)
    expr = sp.sympify(args.expr, locals=local_dict)
    expected = sp.sympify(args.expected, locals=local_dict)
    point = sp.sympify(args.to, locals=local_dict)
    computed = sp.limit(expr, local_dict[args.var], point)
    simplified = sp.simplify(computed - expected)
    passed = simplified == 0
    return CheckResult(
        "PASS" if passed else "FAIL",
        {
            "check": "sympy-limit",
            "expr": args.expr,
            "var": args.var,
            "to": args.to,
            "expected_expr": args.expected,
            "computed_limit": str(computed),
            "simplified_difference": str(simplified),
            "symbols": sorted(local_dict),
        },
    )


def render_markdown(result: CheckResult) -> str:
    lines = [f"Status: `{result.status}`", "", "| Field | Value |", "| --- | --- |"]
    for key, value in result.payload.items():
        rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
        lines.append(f"| `{key}` | `{rendered}` |")
    return "\n".join(lines) + "\n"


def emit(result: CheckResult, fmt: str) -> int:
    if fmt == "json":
        print(json.dumps({"status": result.status, **result.payload}, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result), end="")
    return 0 if result.status == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    subparsers = parser.add_subparsers(dest="command", required=True)

    numeric = subparsers.add_parser("numeric-eq", help="Evaluate lhs and rhs numerically")
    numeric.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    numeric.add_argument("--lhs", required=True)
    numeric.add_argument("--rhs", required=True)
    numeric.add_argument("--values", required=True, help='JSON object, e.g. {"x": 1.0}')
    numeric.add_argument("--tolerance", type=float, default=1e-9)
    numeric.set_defaults(func=numeric_eq)

    diff = subparsers.add_parser("finite-diff", help="Compare a central finite difference to an expected derivative")
    diff.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    diff.add_argument("--expr", required=True)
    diff.add_argument("--var", required=True)
    diff.add_argument("--expected", required=True)
    diff.add_argument("--values", required=True, help='JSON object containing --var and any parameters')
    diff.add_argument("--h", type=float, default=1e-6)
    diff.add_argument("--tolerance", type=float, default=1e-5)
    diff.set_defaults(func=finite_diff)

    grid = subparsers.add_parser("grid-eq", help="Compare lhs and rhs over explicit JSON sample points")
    grid.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    grid.add_argument("--lhs", required=True)
    grid.add_argument("--rhs", required=True)
    grid.add_argument("--points", required=True, help='JSON object or list of objects, e.g. [{"x": 1}]')
    grid.add_argument("--values", help="Optional base JSON object merged into every point")
    grid.add_argument("--tolerance", type=float, default=1e-9)
    grid.set_defaults(func=grid_eq)

    order = subparsers.add_parser("residual-order", help="Estimate approximation residual order over shrinking epsilons")
    order.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    order.add_argument("--exact", required=True)
    order.add_argument("--approx", required=True)
    order.add_argument("--epsilon", required=True, help="Variable name used as the small parameter")
    order.add_argument("--epsilons", required=True, help="JSON list of positive epsilon values")
    order.add_argument("--values", help="Optional base JSON object for non-epsilon parameters")
    order.add_argument("--expected-order", type=float)
    order.add_argument("--tolerance", type=float, default=0.1)
    order.set_defaults(func=residual_order)

    stest = subparsers.add_parser("self-test", help="Run built-in checks without external dependencies")
    stest.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    stest.set_defaults(func=self_test)

    seq = subparsers.add_parser("sympy-eq", help="Simplify lhs - rhs with SymPy")
    seq.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    seq.add_argument("--lhs", required=True)
    seq.add_argument("--rhs", required=True)
    seq.add_argument("--symbols", help="Comma-separated symbol names")
    seq.set_defaults(func=sympy_eq)

    sdiff = subparsers.add_parser("sympy-diff", help="Differentiate with SymPy and compare to expected expression")
    sdiff.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    sdiff.add_argument("--expr", required=True)
    sdiff.add_argument("--var", required=True)
    sdiff.add_argument("--expected", required=True)
    sdiff.add_argument("--symbols", help="Comma-separated symbol names")
    sdiff.set_defaults(func=sympy_diff)

    slim = subparsers.add_parser("sympy-limit", help="Compute a one-variable limit with SymPy")
    slim.add_argument("--format", choices=["markdown", "json"], default=argparse.SUPPRESS)
    slim.add_argument("--expr", required=True)
    slim.add_argument("--var", required=True)
    slim.add_argument("--to", required=True)
    slim.add_argument("--expected", required=True)
    slim.add_argument("--symbols", help="Comma-separated symbol names")
    slim.set_defaults(func=sympy_limit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
    except Exception as exc:  # noqa: BLE001 - CLI should report concise failures.
        payload = {
            "status": "ERROR",
            "check": args.command,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        if args.format == "json":
            print(json.dumps(payload, indent=2, ensure_ascii=False), file=sys.stderr)
        else:
            print(render_markdown(CheckResult("ERROR", payload)), file=sys.stderr, end="")
        return 2
    return emit(result, args.format)


if __name__ == "__main__":
    raise SystemExit(main())
