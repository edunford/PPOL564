# Splitting Data and Cross Validation

from sklearn.model_selection import train_test_split # Train-test split
from sklearn.model_selection import LeaveOneOut # Leave One Out Cross Validation
from sklearn.model_selection import KFold # K-fold Cross validation
import pandas as pd

# Visualization
from plotnine import *
import warnings
warnings.filterwarnings("ignore")

# Data
from gapminder import gapminder as gap




# %% -----------------------------------------

# Splitting Data into a training and test data set

y = gap['lifeExp'] # Clarify outcome
X = gap[['gdpPercap','pop']] # Clarify predictors

# Split
splits = train_test_split(X,y,test_size=0.25, random_state=123)


type(splits)
len(splits)

splits[0].shape # Training predictors
splits[1].shape # Test predictors
splits[2].shape # Training outcome
splits[3].shape # test outcome


# unpack all in one step
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25, random_state=123)

# Proportions are split up as expected
X_train.shape[0]/gap.shape[0]
X_test.shape[0]/gap.shape[0]





# %% -----------------------------------------

# Let's look at the splits and see how the randomness worked

d = (gap.merge(X_train.assign(set = 'train')[['set']],
               left_index=True,right_index=True,how="outer")
     .fillna({'set':'test'}))

(
    ggplot(d,aes(x="year",y="country",color="set")) +
    geom_point() +
    theme(figure_size=(10,20))
)






# %% -----------------------------------------

# Leave One Out Cross Validation

# Initialize the splits
loo = LeaveOneOut()

# Split the data
loo_splits = loo.split(X_train)

# Let's look at the splits
n_models =0
for train, test in loo_splits:
    print(f"N Obs. to train on = {train.shape[0]}, N obs to test on = {test.shape[0]}") #
    n_models += 1 # Count the number of models
print(f"Total numbers of models run = {n_models}")







# %% -----------------------------------------

# K-Fold Cross Validation

# Intialize the K-Folds (splits)
kf = KFold(n_splits=5)

# Split the data
k_splits = kf.split(X_train)

# Let's look at the splits
n_models =0
for train, test in k_splits:
    print(f"N Obs. to train on = {train.shape[0]}, N obs to test on = {test.shape[0]}") #
    n_models += 1 # Count the number of models

print(f"Total numbers of models run = {n_models}")






# %% markdown -----------------------------------------

## Many variations on cross-validation; see [**readings**](https://scikit-learn.org/stable/modules/cross_validation.html)
