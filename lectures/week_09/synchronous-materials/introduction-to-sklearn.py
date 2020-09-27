# Introduction to the SKLEARN API

# https://scikit-learn.org/stable/tutorial/basic/tutorial.html
#!pip install scikit-learn


import pandas as pd
from palmerpenguins import load_penguins
from sklearn.linear_model import LinearRegression


# %% -----------------------------------------

############################
########### Data ###########
############################


# Let's load the palmerpenguins data from visualization week as some simple example data.
dat = load_penguins().dropna()
dat.head()

# Break the data up into an outcome and feature set

# Outcome (thing we're trying to predict)
y = dat.body_mass_g.values

# Predictors (information we're using to predict with)
X = dat.filter(['flipper_length_mm','bill_depth_mm']).values


# %% -----------------------------------------

#############################
########### Model ###########
#############################

# The modeling API follows the same frame work (despite the model)

# Instantiate the modeling object
model = LinearRegression()

# Fit the model
model.fit(X,y)

# Fit statistic (metric for how wrong we are) -- R^2
model.score(X,y)

# Generate a predication (i.e. y-hat)
y_hat = model.predict(X)


# %% -----------------------------------------

###################################
########### Performance ###########
###################################

# SKLEARN has a bunch of performance metrics that we can then use to evaluate our models.
from sklearn.metrics import mean_squared_error, r2_score
import math

# R^2
r2_score(y,y_hat).round(2)

# Root mean squared error
math.sqrt(mean_squared_error(y,y_hat))
