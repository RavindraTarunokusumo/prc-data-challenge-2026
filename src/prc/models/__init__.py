"""Model registry. A model is `fit_predict(feats, params, seed) -> pl.DataFrame`
returning [MVT_ID_mvt, pred] for the validation rows (role == 'val') of `feats`.

`feats` comes from a feature-set function in prc.features applied to a fold's masked
view: training rows carry the target in `y`, validation rows have `y` null.
"""

from prc.models import baselines, gbm, linear, routed

REGISTRY = {
    "global_mean": baselines.global_mean,
    "airport_median": baselines.airport_median,
    "airport_hour_median": baselines.airport_hour_median,
    "anchor_aobt3": baselines.anchor_aobt3,
    "ridge": linear.ridge,
    "lightgbm": gbm.lightgbm,
    "xgboost": gbm.xgboost,
    "routed_lightgbm": routed.routed_lightgbm,
}
