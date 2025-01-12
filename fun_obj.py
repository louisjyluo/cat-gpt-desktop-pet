import numpy as np
from scipy.optimize.optimize import approx_fprime
from scipy.special import logsumexp
from utils import ensure_1d

"""
Implementation of function objects.
Function objects encapsulate the behaviour of an objective function that we optimize.
Simply put, implement evaluate(w, X, y) to get the numerical values corresponding to:
f, the function value (scalar) and
g, the gradient (vector).

Function objects are used with optimizers to navigate the parameter space and
to find the optimal parameters (vector). See optimizers.py.
"""


class FunObj:
    """
    Function object for encapsulating evaluations of functions and gradients
    """

    def evaluate(self, w, X, y):
        """
        Evaluates the function AND its gradient w.r.t. w.
        Returns the numerical values based on the input.
        IMPORTANT: w is assumed to be a 1d-array, hence shaping will have to be handled.
        """
        raise NotImplementedError("This is a base class, don't call this")

    def check_correctness(self, w, X, y):
        n, d = X.shape
        w = ensure_1d(w)
        y = ensure_1d(y)

        estimated_gradient = approx_fprime(
            w, lambda w: self.evaluate(w, X, y)[0], epsilon=1e-6
        )
        _, implemented_gradient = self.evaluate(w, X, y)
        difference = estimated_gradient - implemented_gradient
        if np.max(np.abs(difference) > 1e-4):
            print(
                "User and numerical derivatives differ: %s vs. %s"
                % (estimated_gradient, implemented_gradient)
            )
        else:
            print("User and numerical derivatives agree.")

class SoftmaxLoss(FunObj):
    def evaluate(self, w, X, y):
        w = ensure_1d(w)
        y = ensure_1d(y)

        n, d = X.shape
        k = len(np.unique(y))
        W = w.reshape(k, d)
    
        XW = X @ W.T

        logsumexp_XW = logsumexp(XW, axis=1)

        p = np.exp(XW - logsumexp_XW[:, np.newaxis])

        one_hots = np.eye(k)[y]
        Xw_of_y = XW[np.arange(n), y] 
        f = -Xw_of_y.sum() + logsumexp_XW.sum()

        G = np.einsum('ij, ic -> cj', X, p - one_hots)
        g = G.reshape(-1)
        return f + 1/2 * W.T.flatten() @ W.flatten(), g + 1 * W.flatten()