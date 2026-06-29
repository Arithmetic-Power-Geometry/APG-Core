"""Validate APG local closure-defect first-order approximation for (a,b)=(3,4)."""

from apg_core import local_closure_defect, local_first_order_approximation, squared_weights, shannon_entropy

A, B = 3, 4
weights = squared_weights([A, B])
print("weights:", weights)
print("H(W):", shannon_entropy(weights))
print()
print("n\texact_delta\tfirst_order\tresidual")

for n in [1.8, 1.9, 1.95, 2.0, 2.05, 2.1, 2.2]:
    exact = local_closure_defect(A, B, n)
    approx = local_first_order_approximation(A, B, n)
    print(f"{n:.2f}\t{exact:.8f}\t{approx:.8f}\t{abs(exact-approx):.8f}")
