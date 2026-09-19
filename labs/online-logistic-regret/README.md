# Online Logistic Regret Lab

A falsification-first lab for online binary logistic regression.

## Research target

At round t:
1. observe x_t in R^d with ||x_t||_2 <= R;
2. predict a real logit z_t (the learner may be improper);
3. observe y_t in {-1,+1};
4. incur log(1+exp(-y_t z_t)).

Comparator class: linear predictors theta with ||theta||_2 <= B.

Regret:
R_T(theta)=sum_t ell(z_t,y_t)-sum_t ell(<theta,x_t>,y_t).

### Baseline facts to reproduce

- Proper ONS: logarithmic T dependence but exponential dependence on BR in the worst-case curvature constant.
- Improper/mixable predictors: near-minimax O(d log(BT)) regret is known.
- The current research question is therefore computational: can near-minimax regret be attained by a genuinely lightweight sequential algorithm (target: roughly O(d^2) work per round), rather than high-degree sampling complexity?

This branch does **not** claim that question is solved.

## Run

```bash
python experiments/adversarial_1d.py --T 100 300 1000 --B 5 --trials 200
```

The experiment compares:
- discretized Bayesian/mixability prediction (1-D numerical reference);
- projected OGD;
- a simple proper ONS baseline;
- the best bounded linear comparator in hindsight.

The random search deliberately looks for sequences that maximize regret.

## Scientific stop rule

A breakthrough is recorded only if:
1. a theorem is proved under explicit assumptions;
2. known lower bounds are not contradicted;
3. adversarial search fails to falsify it;
4. the claim is checked against current literature;
5. code and workflow reproduce the evidence.

Until then, all candidate bounds are hypotheses.
