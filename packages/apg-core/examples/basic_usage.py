"""Basic APG-Core usage example."""

from apg_core import descriptor_summary

x = [3, 4, 5]
summary = descriptor_summary(x, exponents=[2.5, 3, 4])

print("APG descriptor summary")
for key, value in summary.items():
    print(f"{key}: {value}")
