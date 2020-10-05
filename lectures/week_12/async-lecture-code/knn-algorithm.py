'''
KNN from Scratch
'''

import numpy as np
import pandas as pd
from plotnine import *
from sklearn.model_selection import train_test_split
import sklearn.metrics as m

# %% -----------------------------------------


dat = pd.read_csv("turnout.csv")
y = dat['vote'].values
X = dat.drop(columns=['vote','id']).values


# Split the data.
train_X,test_X,train_y,test_y = train_test_split(X,y,test_size=0.25, random_state=123)


# %% -----------------------------------------


class KNN:
    '''
    Implementation of the K-Nearest Neighbors Algorithm
    '''

    def __init__(self,train_X,train_y,k=3):
        self.X = train_X # Training predictors
        self.y = train_y # Training outcome
        self.k = k       # N nearest neighbors to consider


    def distance(self,loc1,loc2):
        """Calculate euclidean distance.

        Args:
            loc1 (list): row of data.
            loc2 (list): row of data.

        Returns:
            float: euclidean distance of the two provided data points.
        """
        squared_distance = [(loc1[i] - loc2[i])**2 for i in range(len(loc1))]
        sum_squared_distance = sum(squared_distance)
        euclidean_distance = np.sqrt(sum_squared_distance)
        return euclidean_distance



    def get_neighbors(self,test_row):
        """Calculate the distance between a test data point and the
        training data to generate a prediction.

        Args:
            test_row (list): row of test data to locate neighbors from the training data
                for to generate a prediction.

        Returns:
            numpy array: matrix of distance and outcome data for the k nearest
                data points from the training data.
        """

        distances = list() # store the distances

        # iterate through each row of the training data.
        for i, train_row in enumerate(self.X):
            # Calculate the distance between the training data
            # And the test row.
            d = self.distance(train_row,test_row)

            # Append the data entry on.
            distances.append([d,self.y[i]])

        # Sort in ascending order to calculate the nearest neighbors
        distances.sort()

        # Calculate the number of k nearest neighbors.
        nearest_neighbors = distances[:self.k]

        # Return data as a numpy array
        return np.array(nearest_neighbors)



    def generate_prediction(self,nearest_neighbors):
        """Generate a prediction for the new row of data. If a classification problem,
        returns the predicted probability by taking a majority vote of the nearest
        training data. If a regression problem, calculates the average y from the
        nearest training data.

        Args:
            nearest_neighbors (numpy array): matrix of distance and outcome values of the k
                nearest observations from the training data.

        Returns:
            float: returns an average prediction from the outcome of the nearest training data.

        """
        prediction = nearest_neighbors[:,1].mean()
        return prediction


    def fit(self,test_X):
        """Main implementation of the K Nearest Neighbors Algorithm.

        Args:
            test_X (numpy array): matric of new data to generate a prediction for.
        """

        # Store predictions
        predictions = list()

        # Iterate through each row of the new data.
        for test_row in test_X:
            # Calculate the nearest neightbors
            neighbors = self.get_neighbors(test_row)

            # Generate a prediction
            pred = self.generate_prediction(neighbors)

            # Story the prediction
            predictions.append(pred)

        # store predictions
        self.predictions = np.array(predictions)




# %% -----------------------------------------

# Implementation
mod = KNN(train_X=train_X,train_y = train_y,k = 5)
mod.fit(test_X) # Fit the model to the test data.

# Convert to a class
prob = mod.predictions
pred = 1*(prob >= .5)

# Performance
m.accuracy_score(test_y,pred)
m.roc_auc_score(test_y,prob)
m.confusion_matrix(test_y,pred)



# %% -----------------------------------------


# Example of overfitting an underfitting using KNN

# Fake data
np.random.seed(123)
N = 200
x = np.random.normal(size=N)
z = np.random.normal(size=N)
e = np.random.normal(size=N,scale=3)
y = 1 + x + -1.5*x**2 + np.sin(x) + e
D = pd.DataFrame(dict(y=y,x=x))





# %% -----------------------------------------


# Plot the data
(
    ggplot(D,aes(x="x",y="y")) +
    geom_point() +
    theme(figure_size=(10,5))
)

# %% -----------------------------------------

# Run the algorithms for different values of K.

X = D.drop(columns=['y']).values
Y = D['y'].values

# Fit our knn model
mod = KNN(train_X=X,train_y = Y,k = 1)
mod.fit(X) # Fit the model
D['prediction k=1'] = mod.predictions # Save the predictions

mod = KNN(train_X=X,train_y = Y,k = 5)
mod.fit(X) # Fit the model
D['prediction k=5'] = mod.predictions # Save the predictions

mod = KNN(train_X=X,train_y = Y,k = 25)
mod.fit(X) # Fit the model
D['prediction k=25'] = mod.predictions # Save the predictions


# %% -----------------------------------------

# Plot the data with the different fits on them.
(
    ggplot(D,aes(x="x",y="y")) +
    geom_point(alpha=.5) +
    geom_line(D,aes(x="x",y='prediction k=1'),
              color="orange",size=1,alpha=.5) +
    geom_line(D,aes(x="x",y='prediction k=5'),
              color="darkred",size=1.5,alpha=.75) +
    geom_line(D,aes(x="x",y='prediction k=25'),
              color="forestgreen",size=1.5,alpha=.75) +
    theme(figure_size=(10,5))
)
