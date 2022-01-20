import pandas as pd
from path import Path
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import pymongo
from pymongo import MongoClient
import pandas as pd
from pandas import DataFrame

def model(collection):
    all_records = collection.find()
    list_cursor = list(all_records)

    app_data = pd.DataFrame(list_cursor)
    # Set the index to the App Name moving forward
    app_data = app_data.set_index('App Name')

    # Dropped the _id column did not add to the data
    app_data = app_data.drop(["_id"],axis=1)
    app_data = app_data.drop(app_data.columns[0], axis=1)

    # Qualified apps as good using median of rating and max installs and higher than 250 rating count.
    app_data['Good_App'] = np.where((app_data['Rating']>=4.2) & (app_data['Rating Count']>=250) & (app_data['Maximum Installs']>=43901.5),1,0)

    # Restructured the Released column to datetime
    app_data['Released'] = pd.to_datetime(app_data['Released'])

    # Extracted the month number from the Released column
    app_data['Month_Num'] = app_data['Released'].dt.month

    # Encoded the Category column so that it could be used in the machine learning
    app_data_encoded = pd.get_dummies(app_data, columns=['Category'])

    # Dropped the Released and Size (Mb) columns
    app_data_encoded = app_data_encoded.drop(['Released','Size (Mb)'],axis=1)

    data_scaler = StandardScaler()
    app_data_scaled = data_scaler.fit_transform(app_data_encoded)

    X = app_data_encoded.copy()
    X = X.drop(["Rating","Rating Count","Maximum Installs","Good_App","App Name"], axis=1)

    y = app_data_encoded["Good_App"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=78)

    # Creating a StandardScaler instance
    scaler = StandardScaler()
    # Fitting the Standard Scaler with the training data
    X_scaler = scaler.fit(X_train)

    # Scaling the data
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)

    # Creating the decision tree classifier instance.
    model = tree.DecisionTreeClassifier()
    # Fitting the model.
    model = model.fit(X_train_scaled, y_train)

    # Making predictions using the testing data.
    predictions = model.predict(X_test_scaled)

    # Calculating the confusion matrix
    cm = confusion_matrix(y_test, predictions)

    # Create a DataFrame from the confusion matrix.
    cm_df = pd.DataFrame(
    cm, index=["Actual 0", "Actual 1"], columns=["Predicted 0", "Predicted 1"])

    # Calculating the accuracy score.
    acc_score = accuracy_score(y_test, predictions)

    return print(cm_df)