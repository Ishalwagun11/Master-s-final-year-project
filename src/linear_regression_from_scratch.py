"""
Linear regression from scratch — verifying the math we derived by hand.

We check three things all agree:
  1. The single-variable formulas:  w = cov(x,y)/var(x),  b = ybar - w*xbar
  2. The matrix normal equation:     w = (X^T X)^-1 X^T y
  3. Sanity check against NumPy's own least-squares solver.
"""

import numpy as np

# --- Make some fake data with a known true line: y = 3x + 2 (+ noise) ---
rng = np.random.default_rng(0)
x = np.linspace(0, 10, 50)
y = 3 * x + 2 + rng.normal(0, 1, size=x.shape)   # true slope 3, intercept 2


# --- Layer 1: the calculus formulas, one feature ---------------------------
xbar, ybar = x.mean(), y.mean()
w1 = np.sum((x - xbar) * (y - ybar)) / np.sum((x - xbar) ** 2)   # slope
b1 = ybar - w1 * xbar                                             # intercept
print(f"Layer 1 (calculus):     slope = {w1:.4f},  intercept = {b1:.4f}")


# --- Layer 2: the matrix normal equation -----------------------------------
# Build X with a leading column of 1's so the intercept is just another weight.
X = np.column_stack([np.ones_like(x), x])        # shape (50, 2)
w_vec = np.linalg.inv(X.T @ X) @ X.T @ y         # w = (X^T X)^-1 X^T y
print(f"Layer 2 (normal eqn):   slope = {w_vec[1]:.4f},  intercept = {w_vec[0]:.4f}")


# --- Layer 3: trust-but-verify against NumPy's solver ----------------------
w_np, *_ = np.linalg.lstsq(X, y, rcond=None)
print(f"Layer 3 (numpy lstsq):  slope = {w_np[1]:.4f},  intercept = {w_np[0]:.4f}")

print("\nAll three should match — and land near the true slope=3, intercept=2.")
