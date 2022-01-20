from urllib import request
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
from IPython.display import HTML
import app
import cgi
from flask import Flask, render_template, redirect, url_for


def clean_data(collection):
    hundred = collection.find().limit(500)
    list_cursor = list(hundred)
    app_data = pd.DataFrame(list_cursor)

    # Set the index to the App Name moving forward
    # app_data = app_data.set_index('App Name')

    # Dropped the _id column did not add to the data
    app_data = app_data.drop(["_id"],axis=1)
    app_data = app_data.drop(app_data.columns[0], axis=1)

    # Qualified apps as good using median of rating and max installs and higher than 250 rating count.
    app_data['Good_App'] = np.where((app_data['Rating']>=4.2) & (app_data['Rating Count']>=250) & (app_data['Maximum Installs']>=43901.5),1,0)

    return app_data

def clean_data2(collection):
    hundred = collection.find().limit(5)
    list_cursor = list(hundred)
    app_data = pd.DataFrame(list_cursor)

    category = request.form['category']
    df_filtered = app_data.loc[app_data["category"] == category]

    return print(df_filtered)

# def subset(category): 
#   app_data = clean_data(app.no_good_app_collection)
#   df_subset = app_data.loc[app_data['Category'] == category]
# #  & (app_data['Rating'] >= rating) & (app_data['Price'] <= price)
# #                         & (app_data['Released Date'] == released_date) & (app_data['Released Date'] == released_date) & 
# #                         (app_data['Ad Supported'] == ad_supported) & (app_data['In App Purchases'] == in_app_purchases)]
#   return df_subset