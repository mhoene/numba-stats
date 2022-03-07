"""
Exponential distribution.
"""
import numpy as np
from math import expm1 as _expm1, log1p as _log1p
from ._util import _jit, _trans, _generate_wrappers


@_jit(-1)
def _cdf1(z):
    return -_expm1(-z)


@_jit(-1)
def _ppf1(p):
    return -_log1p(-p)


@_jit(2)
def _logpdf(x, loc, scale):
    """
    Return log of probability density.
    """
    z = _trans(x, loc, scale)
    return -z - np.log(scale)


@_jit(2)
def _pdf(x, loc, scale):
    """
    Return probability density.
    """
    return np.exp(_logpdf(x, loc, scale))


@_jit(2)
def _cdf(x, loc, scale):
    """
    Return cumulative probability.
    """
    z = _trans(x, loc, scale)
    for i, zi in enumerate(z):
        z[i] = _cdf1(zi)
    return z


@_jit(2)
def _ppf(p, loc, scale):
    """
    Return quantile for given probability.
    """
    z = np.empty_like(p)
    for i, pi in enumerate(p):
        z[i] = _ppf1(pi)
    return scale * z + loc


_generate_wrappers(globals())
