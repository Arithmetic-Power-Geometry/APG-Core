import math
import pytest

from apg_core import (
    APGError,
    squared_weights,
    shannon_entropy,
    renyi_entropy,
    concentration,
    power_defect,
    shannon_renyi_upper_bound,
    linear_entropy_bound,
    concentration_lower_bound,
    local_closure_defect,
    local_first_order_approximation,
    integrated_defect_bound,
    descriptor_summary,
)


def test_squared_weights_3_4():
    w = squared_weights([3, 4])
    assert pytest.approx(sum(w), abs=1e-12) == 1.0
    assert pytest.approx(w[0], abs=1e-12) == 9 / 25
    assert pytest.approx(w[1], abs=1e-12) == 16 / 25


def test_entropy_3_4():
    w = squared_weights([3, 4])
    h = shannon_entropy(w)
    expected = -((9 / 25) * math.log(9 / 25) + (16 / 25) * math.log(16 / 25))
    assert pytest.approx(h, abs=1e-12) == expected


def test_concentration():
    assert pytest.approx(concentration([0.2, 0.8]), abs=1e-12) == 0.8


def test_renyi_alpha_one_matches_shannon():
    w = [0.25, 0.75]
    assert pytest.approx(renyi_entropy(w, 1), abs=1e-12) == shannon_entropy(w)


def test_power_defect_at_two_is_zero():
    w = squared_weights([3, 4, 5])
    assert pytest.approx(power_defect(w, 2), abs=1e-12) == 0.0


def test_bounds_order():
    w = squared_weights([3, 4, 5])
    for t in [2.5, 3, 4]:
        d = power_defect(w, t)
        lb = concentration_lower_bound(w, t)
        ub = shannon_renyi_upper_bound(w, t)
        lin = linear_entropy_bound(w, t)
        assert lb <= d + 1e-12
        assert d <= ub + 1e-12
        assert ub <= lin + 1e-12


def test_local_closure_defect_zero_at_two():
    assert pytest.approx(local_closure_defect(3, 4, 2), abs=1e-12) == 0.0


def test_local_first_order_close_near_two():
    exact = local_closure_defect(3, 4, 2.01)
    approx = local_first_order_approximation(3, 4, 2.01)
    assert abs(exact - approx) < 1e-5


def test_integrated_bound_positive():
    w = squared_weights([3, 4])
    assert integrated_defect_bound(w, 3) > 0


def test_descriptor_summary_keys():
    result = descriptor_summary([3, 4], exponents=[3])
    assert "weights" in result
    assert "entropy" in result
    assert "concentration" in result
    assert "D_3" in result


def test_invalid_values_raise():
    with pytest.raises(APGError):
        squared_weights([0, 1])
    with pytest.raises(APGError):
        power_defect([0.5, 0.5], 1.5)
