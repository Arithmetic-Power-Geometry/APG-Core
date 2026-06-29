"""APG-Core: Core Computational Descriptors for Arithmetic Power Geometry."""

from .descriptors import (
    APGError,
    squared_weights,
    shannon_entropy,
    renyi_entropy,
    concentration,
    power_sum,
    power_defect,
    shannon_renyi_upper_bound,
    linear_entropy_bound,
    concentration_lower_bound,
    local_closure_defect,
    local_first_order_approximation,
    integrated_defect_bound,
    descriptor_summary,
)

__author__ = "Dr. Mohammad Amir Khusru Akhtar"
__email__ = "akakhtar.2024@gmail.com"
__version__ = "1.0.0"

__all__ = [
    "APGError",
    "squared_weights",
    "shannon_entropy",
    "renyi_entropy",
    "concentration",
    "power_sum",
    "power_defect",
    "shannon_renyi_upper_bound",
    "linear_entropy_bound",
    "concentration_lower_bound",
    "local_closure_defect",
    "local_first_order_approximation",
    "integrated_defect_bound",
    "descriptor_summary",
]
