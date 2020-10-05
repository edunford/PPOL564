'''
Decision Tree from Scratch
'''



import numpy as np
import pandas as pd
from plotnine import *
from sklearn.model_selection import train_test_split
import sklearn.metrics as m
from gapminder import gapminder as dat

# %% -----------------------------------------


# Predict life expectancy using the Gapminder data
y = dat['lifeExp']
X = (dat
     .eval("ln_pop = log(pop)")
     .eval("ln_gdp = log(gdpPercap)")
     .eval("cold_war = 1*(year < 1990)")
     [['ln_pop','ln_gdp','cold_war']]
     )


# Split the data.
train_X,test_X,train_y,test_y = train_test_split(X,y,test_size=0.25, random_state=123)


# %% -----------------------------------------

class DecisionTree:
    '''
    Implementation of the decision tree algorithm.
    '''

    def __init__(self,train_X,train_y,max_depth=3):
        self.X = train_X # Training predictors
        self.y = train_y # Training outcome
        self.max_depth = max_depth # How deep should the tree grow? This is an important tuning parameter


    def rss(self,y):
        '''
        Residual sum of squares.
        '''
        return np.sum((y - np.mean(y)) ** 2)


    def cost(self,y_left,y_right):
        '''
        Tree cost function: residual sum of squares for both branches.
        '''
        return self.rss(y_left) + self.rss(y_right)


    def find_rule(self,X,y):
        '''
        Find the split rule. That is, which feature and which threshold of the potential
        values that feature takes on should we split the data by.

        Returns:
            dict: containing the feature and split rule.
        '''

        # initialize the objects
        best_feature = None # empyt
        best_threshold = None # empty
        min_rss = np.inf # Set the error high...

        # For all available features, find the feature that when split
        # minimizes residual sum of squares
        for feature in X.columns:

            # All unique values the selected feature can take on.
            thresholds = X[feature].unique().tolist()
            thresholds.sort() # Sort the threshold values in ascending order
            # drop the first value (when splitting we need values on left and right.)
            thresholds = thresholds[1:]

            # Iterate through the thresholds
            for t in thresholds:

                # Data below the threshold goes on the left
                y_left_ix = X[feature] < t # this is a boolean array

                # the reset fo the data goes on the right.
                y_left, y_right = y[y_left_ix], y[~y_left_ix]

                # Calculate the rss for both sides.
                t_rss = self.cost(y_left, y_right)

                # If the error is less than the current min, record the split rule information
                if t_rss < min_rss:
                    min_rss = t_rss # Save the new minimum (only changes if we can beat it)
                    best_threshold = t # Save the new threshold
                    best_feature = feature # Save the relevant feature


        # Return the feature and the split that minimizes the error.
        return {'feature': best_feature, 'threshold': best_threshold}


    def split(self,X, y, depth):
        '''
        Recursive spliting: split the data up until we reach our stop rule
        dictated by the max depth.
        '''

        # Stopping rule: if we reach the maximum depth
        # OR if there are only two observations left in the node.
        # Return prediction (average y)
        if depth == self.max_depth or len(X) < 2:
            return {"prediction": np.mean(y)}

        # Find the split rule
        rule = self.find_rule(X,y)

        # If data is below the rule, then push to the left node, else go left.
        # Remember that the output of the find_rule() is a dictionary.
        left_ix = X[rule['feature']] < rule['threshold']

        # Recursive Part: split data then call a smaller subset of the data.
        # The depth moves us toward the max_depth (the stopping rule!); This
        # little piece causes the recursion to stop.

        # Go left
        rule['left'] = self.split(X[left_ix], y[left_ix], depth + 1)

        # Go right
        rule['right'] = self.split(X[~left_ix], y[~left_ix], depth + 1)

        # Once the stoping rule is hit, the rules are returned (with the prediction attached
        # to the terminal notes)
        return rule

    def fit(self):
        '''
        Fit the decision tree model using the training data.
        '''
        # recursively split the data and store the split rules.
        self.split_rules = self.split(self.X, self.y, depth = 0)


    def generate_prediction(self,test_row):
        '''
        Make predictions on new (test) observation. use the test data to trace
        the decision tree to make a prediction.
        '''

        prediction = None

        # Copy the split rules
        rules = self.split_rules.copy()

        while prediction is None:

            # Select the feature and the split
            feature = rules['feature']
            threshold = rules['threshold']

            # If below the threhold, go left
            if test_row[feature] < threshold:
                rules = rules['left']
            else: # else go right
                rules = rules['right']

            # If you hit a terminal node, there will be a prediction key
            # If not, return none and continue the while loop
            prediction = rules.get('prediction')

        # Return the prediction from the tree
        return prediction


    def predict(self,test_X):
        '''
        Make a prediction on every observation in the test dataset
        '''
        # Store all the predictions for the new test data
        predictions = list()

        # Iterate through each row in the test data
        for i, test_row in test_X.iterrows():

            # Generate a prediction for this row of data
            pred = self.generate_prediction(test_row)

            # Append the prediction to the data.
            predictions.append(pred)

        # Return the array of predicted values
        return np.array(predictions)






# %% -----------------------------------------



# Test Implementation.
mod = DecisionTree(train_X= train_X,train_y=train_y,max_depth=4)
mod.fit()

# Look at the split rules
mod.split_rules


# Make a prediction
y_hat = mod.predict(test_X)


# Examine out-of-sample performance
m.r2_score(test_y,y_hat)
m.mean_absolute_error(test_y,y_hat)



# %% -----------------------------------------

# Printing the Decision Rules

def print_tree_rules(rules,indent=0,digit=2):
    '''
    Recursively print the decision tree rules.
    '''
    pred = rules.get('prediction')
    if pred is not None:
        print('\t'*indent + f"y = {round(pred,digit)}",end="\n")
    else:
        print('\t'*indent + f"IF {rules['feature']} < {round(rules['threshold'],digit)}")
        print_tree_rules(rules['left'],indent=indent + 1)
        print('\t'*indent + "ELSE")
        print_tree_rules(rules['right'],indent=indent + 1)


# Print the rules.
print("DECISION RULES\n")
print_tree_rules(mod.split_rules)
