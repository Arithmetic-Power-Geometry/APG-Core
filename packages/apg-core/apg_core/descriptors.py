"""
Core computational descriptors for Arithmetic Power Geometry (APG).

APG studies structural deformation under continuous exponent variation.
This module implements the reusable descriptor layer used across APG
applications: squared Euclidean weights, Shannon entropy, concentration,
Renyi entropy, power-sum defects, and local closure defects.

Author: Dr. Mohammad Amir Khusru Akhtar
License: GPL-3.0-or-later
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence, Union, List, Dict, Any

Number = Union[int, float]


class APGError(ValueError):
    """Raised when APG input validation fails."""


def _as_positive_float_list(values: Iterable[Number], *, name: str = "values") -> List[float]:
    """Convert an iterable to a list of positive finite floats."""
    try:
        data = [float(v) for v in values]
    except TypeError as exc:
        raise APGError(f"{name} must be an iterable of positive real numbers.") from exc

    if not data:
        raise APGError(f"{name} must not be empty.")
    for v in data:
        if not math.isfinite(v):
            raise APGError(f"{name} must contain only finite real numbers.")
        if v <= 0:
            raise APGError(f"{name} must contain only positive real numbers.")
    return data


def squared_weights(values: Iterable[Number]) -> List[float]:
    """
    Compute normalized squared Euclidean APG weights.

    For X=(x_1,...,x_m), APG uses
        w_i = x_i^2 / sum_j x_j^2.

    Parameters
    ----------
    values:
        Positive real coordinates.

    Returns
    -------
    list[float]
        Probability vector summing to 1 up to floating-point precision.
    """
    data = _as_positive_float_list(values, name="values")
    denom = sum(v * v for v in data)
    if denom <= 0 or not math.isfinite(denom):
        raise APGError("sum of squared coordinates must be finite and positive.")
    return [(v * v) / denom for v in data]


def shannon_entropy(weights: Iterable[Number], *, normalize: bool = False) -> float:
    """
    Compute Shannon entropy H(W) = -sum_i w_i log(w_i), in nats.

    Parameters
    ----------
    weights:
        Positive probability weights. They do not need to sum exactly to 1;
        they will be normalized internally.
    normalize:
        If True, divide by log(m), returning entropy in [0, 1] for m>1.

    Returns
    -------
    float
        Shannon entropy in nats, or normalized entropy if requested.
    """
    w = _normalize_probability(weights)
    h = -sum(p * math.log(p) for p in w if p > 0)
    if normalize:
        return 0.0 if len(w) <= 1 else h / math.log(len(w))
    return h


def renyi_entropy(weights: Iterable[Number], alpha: Number) -> float:
    """
    Compute Renyi entropy of order alpha.

    H_alpha(W) = 1/(1-alpha) log(sum_i w_i^alpha), alpha != 1.
    For alpha = 1, this returns Shannon entropy.
    """
    a = float(alpha)
    if not math.isfinite(a) or a <= 0:
        raise APGError("alpha must be a positive finite real number.")
    w = _normalize_probability(weights)
    if abs(a - 1.0) < 1e-12:
        return shannon_entropy(w)
    return math.log(sum(p ** a for p in w)) / (1.0 - a)


def concentration(weights: Iterable[Number]) -> float:
    """
    Compute APG concentration C_APG = max_i w_i.
    """
    w = _normalize_probability(weights)
    return max(w)


def power_sum(weights: Iterable[Number], exponent: Number) -> float:
    """
    Compute APG power sum S_t(W) = sum_i w_i^(t/2).
    """
    t = _positive_finite(exponent, "exponent")
    w = _normalize_probability(weights)
    return sum(p ** (t / 2.0) for p in w)


def power_defect(weights: Iterable[Number], exponent: Number) -> float:
    """
    Compute normalized multi-variable APG power defect.

        D_m(t) = 1 - sum_i w_i^(t/2),  for t >= 2.

    The defect is 0 at t=2 and grows with exponent deformation in
    concentrated/dispersed weight structures.
    """
    t = _positive_finite(exponent, "exponent")
    if t < 2:
        raise APGError("APG power_defect is defined here for exponent t >= 2.")
    return 1.0 - power_sum(weights, t)


def shannon_renyi_upper_bound(weights: Iterable[Number], exponent: Number) -> float:
    """
    Compute Shannon--Renyi APG upper bound:

        D_m(t) <= 1 - exp(-((t-2)/2) H(W)).
    """
    t = _positive_finite(exponent, "exponent")
    if t < 2:
        raise APGError("bound is defined for exponent t >= 2.")
    h = shannon_entropy(weights)
    return 1.0 - math.exp(-((t - 2.0) / 2.0) * h)


def linear_entropy_bound(weights: Iterable[Number], exponent: Number) -> float:
    """
    Compute linear APG entropy bound:

        D_m(t) <= ((t-2)/2) H(W).
    """
    t = _positive_finite(exponent, "exponent")
    if t < 2:
        raise APGError("bound is defined for exponent t >= 2.")
    return ((t - 2.0) / 2.0) * shannon_entropy(weights)


def concentration_lower_bound(weights: Iterable[Number], exponent: Number) -> float:
    """
    Compute dimension-stable lower bound:

        D_m(t) >= 1 - M^((t-2)/2), where M = max_i w_i.
    """
    t = _positive_finite(exponent, "exponent")
    if t < 2:
        raise APGError("bound is defined for exponent t >= 2.")
    m = concentration(weights)
    return 1.0 - (m ** ((t - 2.0) / 2.0))


def local_closure_defect(a: Number, b: Number, exponent: Number) -> float:
    """
    Compute the APG two-coordinate local closure defect at the Euclidean target.

    Let c_2 = sqrt(a^2+b^2), K_P = n-2. Then
        delta_K = |1 - (a^n+b^n)/(a^2+b^2)^(n/2)|.

    Parameters
    ----------
    a, b:
        Positive base coordinates.
    exponent:
        Positive exponent n.
    """
    aa = _positive_finite(a, "a")
    bb = _positive_finite(b, "b")
    n = _positive_finite(exponent, "exponent")
    denom = (aa * aa + bb * bb) ** (n / 2.0)
    return abs(1.0 - ((aa ** n + bb ** n) / denom))


def local_first_order_approximation(a: Number, b: Number, exponent: Number) -> float:
    """
    Compute first-order APG entropy approximation near n=2:

        delta_K approx (H(W)/2) |n-2|,

    where W=(a^2/(a^2+b^2), b^2/(a^2+b^2)).
    """
    aa = _positive_finite(a, "a")
    bb = _positive_finite(b, "b")
    n = _positive_finite(exponent, "exponent")
    w = squared_weights([aa, bb])
    return 0.5 * shannon_entropy(w) * abs(n - 2.0)


def integrated_defect_bound(weights: Iterable[Number], exponent: Number) -> float:
    """
    Compute quadratic integrated-defect upper bound near n=2:

        A_0 <= H(W)/4 * (n-2)^2.

    This helper implements the bound used in APG Shannon--Renyi control.
    """
    n = _positive_finite(exponent, "exponent")
    if n < 2:
        raise APGError("integrated_defect_bound is implemented for exponent n >= 2.")
    return (shannon_entropy(weights) / 4.0) * ((n - 2.0) ** 2)


def descriptor_summary(values: Iterable[Number], *, exponents: Sequence[Number] = (2.5, 3, 4)) -> Dict[str, Any]:
    """
    Return a compact APG descriptor summary for a positive vector.

    Useful for APG-OOD, APG-fraud, APG-materials, and metric-screening pipelines.
    """
    w = squared_weights(values)
    summary: Dict[str, Any] = {
        "weights": w,
        "entropy": shannon_entropy(w),
        "normalized_entropy": shannon_entropy(w, normalize=True),
        "concentration": concentration(w),
    }
    for t in exponents:
        tt = float(t)
        summary[f"D_{tt:g}"] = power_defect(w, tt)
        summary[f"upper_bound_{tt:g}"] = shannon_renyi_upper_bound(w, tt)
        summary[f"linear_bound_{tt:g}"] = linear_entropy_bound(w, tt)
        summary[f"lower_bound_{tt:g}"] = concentration_lower_bound(w, tt)
    return summary


def _normalize_probability(weights: Iterable[Number]) -> List[float]:
    data = _as_positive_float_list(weights, name="weights")
    total = sum(data)
    if total <= 0 or not math.isfinite(total):
        raise APGError("weights must have a finite positive sum.")
    return [v / total for v in data]


def _positive_finite(value: Number, name: str) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError) as exc:
        raise APGError(f"{name} must be a positive finite real number.") from exc
    if not math.isfinite(v) or v <= 0:
        raise APGError(f"{name} must be a positive finite real number.")
    return v
