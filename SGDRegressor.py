from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


class SGDRegressor():
    def __init__(self, trainingInputs, trainingOutputs, validationInputs, validationOutputs):
        self._validationOutputs = validationOutputs
        self._validationInputs = validationInputs
        self._trainingInputs = trainingInputs
        self._trainingOutputs = trainingOutputs
        self._computedValidationOutputs = []
        self._regressor = linear_model.SGDRegressor(learning_rate='optimal', max_iter=3000)

    def fit(self):
        self._regressor.fit(self._trainingInputs, self._trainingOutputs)
        w0, w1, w2, w3 = self._regressor.intercept_, self._regressor.coef_[0], self._regressor.coef_[1], \
                         self._regressor.coef_[2]
        print('Learnt model: f(x) = ', w0, ' + ', w1, ' * x1 + ', w2, ' * x2', w3, ' * x3')
        return w0, w1, w2, w3

    def validate(self):
        self._computedValidationOutputs = self._regressor.predict(self._validationInputs)
        print('Computed Outputs: ', self._computedValidationOutputs)
        return self._computedValidationOutputs

    def error(self):
        mean_squared = mean_squared_error(self._validationOutputs, self._computedValidationOutputs)
        print("Error: ", mean_squared)

        r2_sc = r2_score(self._validationOutputs, self._computedValidationOutputs)
        print("R2 score: ", r2_sc)

        return mean_squared
