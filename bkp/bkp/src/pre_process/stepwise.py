import statsmodels.api as sm


def stepwise_selection(X, y):
    variables = list(X.columns)
    best_vars = variables.copy()

    while True:
        changed = False
        model = sm.OLS(y, sm.add_constant(X[best_vars])).fit()
        aic_full = model.aic

        aic_with_var_removed = []

        for var in best_vars:
            vars_temp = best_vars.copy()
            vars_temp.remove(var)

            model_temp = sm.OLS(y, sm.add_constant(X[vars_temp])).fit()
            aic_temp = model_temp.aic

            aic_with_var_removed.append((aic_temp, var))

        aic_with_var_removed.sort()
        best_new_aic, worst_var = aic_with_var_removed[0]

        if best_new_aic < aic_full:
            best_vars.remove(worst_var)
            changed = True
        else:
            break

    return best_vars