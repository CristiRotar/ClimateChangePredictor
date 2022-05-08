from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


class LinearRegressor():
    def __init__(self, trainingInputs, trainingOutputs, validationInputs, validationOutputs):
        self._validationOutputs = validationOutputs
        self._validationInputs = validationInputs
        self._trainingInputs = trainingInputs
        self._trainingOutputs = trainingOutputs
        self._computedValidationOutputs = []
        self._regressor = linear_model.LinearRegression()

    def fit(self):
        self._regressor.fit(self._trainingInputs, self._trainingOutputs)
        w0, w1, w2, w3 = self._regressor.intercept_, self._regressor.coef_[0], self._regressor.coef_[1], self._regressor.coef_[2]
        print('Learnt model: f(x) = ', w0, ' + ', w1, ' * x1 + ', w2, ' * x2', w3, ' * x3')
        return w0, w1, w2, w3

    def predict(self):
        self._computedValidationOutputs = self._regressor.predict(self._validationInputs)
        print("Computed Outputs: ", self._computedValidationOutputs)
        return self._computedValidationOutputs

    def error(self):
        error = mean_squared_error(self._validationOutputs, self._computedValidationOutputs)
        print("Error: ", error)

        r2_sc = r2_score(self._validationOutputs, self._computedValidationOutputs)
        print("R2 score: ", r2_sc)

        return error, r2_sc
