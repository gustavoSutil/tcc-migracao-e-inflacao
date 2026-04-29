import statsmodels.api as sm

def forward_selection(data, response, predictors):

    remaining = list(predictors)
    selected = []
    current_score = float("inf")
    best_new_score = float("inf")

    while remaining:
        scores_with_candidates = []

        for candidate in remaining:
            formula = selected + [candidate]

            X = sm.add_constant(data[formula])
            y = data[response]

            model = sm.OLS(y, X).fit()

            aic = model.aic
            scores_with_candidates.append((aic, candidate))

        scores_with_candidates.sort()
        best_new_score, best_candidate = scores_with_candidates[0]

        if best_new_score < current_score:
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
        else:
            break

    return selected