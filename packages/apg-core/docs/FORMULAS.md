# APG-Core Formula Reference

This document records the main formulas implemented in `apg-core`.

## Squared Euclidean weights

For positive coordinates \(X=(x_1,\dots,x_m)\):

\[
w_i=\frac{x_i^2}{\sum_{j=1}^{m}x_j^2}.
\]

## Shannon entropy

\[
H(W)=-\sum_i w_i\log w_i.
\]

## Normalized entropy

\[
H_{norm}(W)=\frac{H(W)}{\log m}.
\]

## Concentration

\[
C_{APG}=\max_i w_i.
\]

## Renyi entropy

For \(\alpha>0, \alpha\ne 1\):

\[
H_\alpha(W)=\frac{1}{1-\alpha}\log\left(\sum_i w_i^\alpha\right).
\]

For \(\alpha=1\), this reduces to Shannon entropy.

## Multi-variable APG power defect

For \(t\ge 2\):

\[
D_m(t)=1-\sum_i w_i^{t/2}.
\]

## Shannon--Renyi control bound

\[
D_m(t)\le 1-\exp\left(-\frac{t-2}{2}H(W)\right)
\le \frac{t-2}{2}H(W).
\]

## Concentration lower bound

\[
D_m(t)\ge 1-M^{(t-2)/2},\quad M=\max_i w_i.
\]

## Local two-coordinate APG closure defect

For \(a,b>0\):

\[
\delta_K(a,b;n)=\left|1-\frac{a^n+b^n}{(a^2+b^2)^{n/2}}\right|.
\]

## First-order local entropy law

Near the Euclidean target \(n=2\):

\[
\delta_K=\frac{H(W)}{2}|n-2|+O((n-2)^2).
\]
