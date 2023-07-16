from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sysidentpy.general_estimators import NARX
from sysidentpy.basis_function._basis_function import Polynomial, Fourier


def LinReg(X, y, n_jobs=-1):
    regressor = LinearRegression()
    regressor.fit(X=X, y=y)
    return regressor


def NARXreg(X, y):
    gb = GradientBoostingRegressor(
        loss='quantile',
        alpha=0.90,
        n_estimators=250,
        max_depth=10,
        learning_rate=.1,
        min_samples_leaf=9,
        min_samples_split=9
    )
    gbnarx = NARX(
        base_estimator = gb,
        xlag=2,
        ylag=2,
        basis_function = Polynomial(degree=2),
        model_type = "NARMAX"
    )
    gbnarx.fit(X=X, y=y)
    return gbnarx
