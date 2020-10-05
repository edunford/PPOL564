# Combining all the ML elements into a pipeline

from sklearn.tree import DecisionTreeRegressor # Select a model (right now the model doesn't matter)
from sklearn.model_selection import train_test_split # Train-test split
from sklearn.model_selection import KFold # K-fold Cross validation
import sklearn.preprocessing as pp
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import sklearn.metrics as m
from sklearn.model_selection import cross_validate

# Data management 
import pandas as pd

# Data
from gapminder import gapminder as gap


# Let's predict life expectancy given GDP and population
y = gap['lifeExp'] # Clarify outcome
X = gap[['gdpPercap','pop']] # Clarify predictors

# %% -----------------------------------------

# split data
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25, random_state=123)


# %% -----------------------------------------

# Combine preprocessing and model together so all steps are run at once
pipe = Pipeline([('scaler', pp.StandardScaler()), ('dtree', DecisionTreeRegressor())])

# Now we can run everything in one pass
pipe.fit(X_train,y_train)

# Make our prediction
y_hat = pipe.predict(X_train)

# See how we did.
m.mean_squared_error(y_train,y_hat)
m.r2_score(y_train,y_hat)

# How well do we do out of sample?
y_hat = pipe.predict(X_test)
m.mean_squared_error(y_test,y_hat)
m.r2_score(y_test,y_hat)

# Not so great. Over fit.


# %% -----------------------------------------

# Fold Cross validation into this process (to estimate the test error using the training data)

kf = KFold(n_splits=5) # Set the number of folds
k_splits = kf.split(X_train) # Create the split generator
scores = [] # Empty list to retain scores

# Loop through the splits, refit the model, and store performance
for train_ind, val_ind in k_splits:

    # Fit Model on the training slits
    pipe.fit(X_train.iloc[train_ind,:],y_train.iloc[train_ind])

    # Predict using the validation splits
    yhat = pipe.predict(X_train.iloc[val_ind,:])

    # Calculate performance scores
    mse = m.mean_squared_error(y_train.iloc[val_ind],yhat)
    r2 = m.r2_score(y_train.iloc[val_ind],yhat)

    # save
    scores.append((mse,r2))


# Convert into DF
dat_scores = pd.DataFrame(scores,columns=["mse","r2"])

# Estimate of test performance
dat_scores.mean(axis=0)



# %% -----------------------------------------

# Is there a quicker way to do this??? Yes!

scores_we_care_about = {"r2":"r2",'mse':'neg_mean_squared_error'}
# List of all the relevant keys: m.SCORERS.keys()


# Use the cross_validation method to validate.
scores = cross_validate(pipe,X=X_train,y=y_train,
                        scoring=scores_we_care_about,
                        cv=5)


# Predicted fit on the test data test error
scores['test_r2'].mean()
-1*scores['test_mse'].mean()


# ISSUE: Note there is one issue with the above. If we want to compare the performance
# of different models (which we often want to do), then we need to ensure that
# the splits for each fold are the same across models (else the difference 
# in performance between two models might just be statistical fluke given 
# how the data was scrambled). 

# How do we get around this? Use the KFold generator to generate consistent folds 
# that we can use again and again 

# By seeding the random state, we can ensure the same folds are generated each time. 
gen_folds = KFold(n_splits=5,random_state=111)  

scores = cross_validate(pipe,X=X_train,y=y_train,
                        scoring=scores_we_care_about,
                        cv=gen_folds) # Just drop the generator in for the cv arg



# %% -----------------------------------------

# Can we do better by adding in country information?


y = gap['lifeExp'] # Clarify outcome
X = gap[['country','gdpPercap','pop']] # Clarify predictors

# split data
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25, random_state=123)


# Different preprocessing transformations given different variable types.
numeric_transformer = Pipeline(steps=[('scaler', pp.StandardScaler())])
categorical_transformer = Pipeline(steps=[('onehot', pp.OneHotEncoder())])

# Combine the different preprocessing instruction, mapping them to specific variables
preprocessor = ColumnTransformer(
    transformers=[('num', numeric_transformer, ['pop','gdpPercap']),
                  ('cat', categorical_transformer, ['country'])]
    )

# Now put it all together into a single pipeline
pipe2 = Pipeline([("preproces",preprocessor), ('dtree', DecisionTreeRegressor())])

# Use the cross_validation method to validate.
scores2 = cross_validate(pipe2,X=X_train,y=y_train,
                        scoring=scores_we_care_about,
                        cv=gen_folds)

# Predicted fit on the test data test error. Country info adds a lot!
scores2['test_r2'].mean()
-1*scores2['test_mse'].mean()
