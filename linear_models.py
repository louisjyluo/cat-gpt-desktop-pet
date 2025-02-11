import numpy as np


class LinearModel:
    """
    Generic linear model, supporting generic loss functions (FunObj subclasses)
    and optimizers.

    See optimizers.py for optimizers.
    See fun_obj.py for loss function objects, which must implement evaluate()
    and return f and g values corresponding to current parameters.
    """

    def __init__(self, loss_fn, optimizer, check_correctness=False):
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.bias_yes = True
        self.check_correctness = check_correctness

        # For debugging and making learning curves
        self.fs = []
        self.nonzeros = []
        self.ws = []

    def optimize(self, w_init, X, y):
        "Perform gradient descent using the optimizer."
        n, d = X.shape

        # Initial guess
        w = np.copy(w_init)
        f, g = self.loss_fn.evaluate(w, X, y)

        # Reset the optimizer state and tie it to the new parameters.
        # See optimizers.py for why reset() is useful here.
        self.optimizer.reset()
        self.optimizer.set_fun_obj(self.loss_fn)
        self.optimizer.set_parameters(w)
        self.optimizer.set_fun_obj_args(X, y)

        # Collect training information for debugging
        fs = [f]
        gs = [g]
        ws = []

        # Use gradient descent to optimize w
        while True:
            f, g, w, break_yes = self.optimizer.step()
            fs.append(f)
            gs.append(g)
            ws.append(w)
            if break_yes:
                break

        return w, fs, gs, ws

    def fit(self, X, y):
        """
        Generic fitting subroutine:
        1. Make initial guess
        2. Check correctness of function object
        3. Use gradient descent to optimize
        """
        n, d = X.shape

        # Correctness check
        if self.check_correctness:
            w = np.random.rand(d)
            self.loss_fn.check_correctness(w, X, y)

        # Initial guess
        w = np.zeros(d)

        # Optimize
        self.w, self.fs, self.gs, self.ws = self.optimize(w, X, y)

    def predict(self, X):
        """
        By default, implement linear regression prediction
        """
        return X @ self.w


class LinearClassifier(LinearModel):
    """
    Generic Logistic Regression classifier,
    whose behaviour is selected by the combination of
    function object and optimizer.
    """

    def predict(self, X):
        return np.sign(X @ self.w)


class LinearClassifierForwardSel(LinearClassifier):
    """
    A logistic regression classifier that trains with forward selection.
    A gradient-based optimizer as well as an objective function is needed.
    """

    def __init__(
        self, local_loss_fn, global_loss_fn, optimizer, check_correctness=False
    ):
        """
        NOTE: There are two loss function objects involved:
        1. local_loss_fn: the loss that we optimize "inside the loop"
        1. global_loss_fn: the forward selection criterion to compare feature sets
        """
        super().__init__(
            loss_fn=local_loss_fn,
            optimizer=optimizer,
            check_correctness=check_correctness,
        )
        self.global_loss_fn = global_loss_fn

    def fit(self, X, y):
        n, d = X.shape

        # Maintain the set of selected indices, as a boolean mask array.
        # We assume that feature 0 is a bias feature, and include it by default.
        selected = np.zeros(d, dtype=bool)
        selected[0] = True
        min_loss = np.inf
        self.total_evals = 0

        # We will hill-climb until a local discrete minimum is found.
        while not np.all(selected):
            old_loss = min_loss
            print(f"Epoch {selected.sum():>3}:", end=" ")

            for j in range(d):
                if selected[j]:
                    continue

                selected_with_j = selected.copy()
                selected_with_j[j] = True

                """YOUR CODE HERE FOR Q2.3"""
                # TODO: Fit the model with 'j' added to the features,
                # then compute the loss and update the min_loss/best_feature.
                # Also update self.total_evals.
                lrl = self.global_loss_fn
                w_init = np.zeros(selected_with_j.sum())
                w, *_ = self.optimize(w_init, X[:, selected_with_j], y)
                f,g = lrl.evaluate(w, X[:, selected_with_j], y)
                if min_loss > f:
                    min_loss = f
                    best_feature = j
                self.total_evals += 1

            if min_loss < old_loss:  # something in the loop helped our model
                selected[best_feature] = True
                print(f"adding feature {best_feature:>3} - loss {min_loss:>7.3f}")
            else:
                print("nothing helped to add; done.")
                break
        else:  # triggers if we didn't break out of the loop
            print("wow, we selected everything")

        w_init = np.zeros(selected.sum())
        w_on_sub, *_ = self.optimize(w_init, X[:, selected], y)
        self.total_evals += self.optimizer.num_evals

        self.w = np.zeros(d)
        self.w[selected] = w_on_sub

class MulticlassLinearClassifier(LinearClassifier):
    """
    LinearClassifier's extention for multiclass classification.
    The constructor method and optimize() are inherited, so
    all you need to implement are fit() and predict() methods.
    """

    def fit(self, X, y):
        n, d = X.shape
        y_classes = np.unique(y)
        k = len(y_classes)
        assert set(y_classes) == set(range(k))  # check labels are {0, 1, ..., k-1}

        # Initial guesses for weights
        w = np.zeros(k * d)
        print("optimizing")
        self.W, *_ = self.optimize(w, X, y)
        

    def predict(self, X_hat):
        n, d = X_hat.shape
        k = 6
        self.W = self.W.reshape(k, d)
        return np.argmax(X_hat @ self.W.T, axis=1)
