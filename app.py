from urllib import request
from flask import Flask
from flask_cors import CORS
import pymongo
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import certifi
import cleaning
import machine_learning
from IPython.display import HTML

ca = certifi.where()

# Replace your URL here. Don't forget to replace the password.
connection_url = "mongodb+srv://mihir123:mihir123@cluster0.yecsu.mongodb.net/test?retryWrites=true&w=majority"
app = Flask(__name__,template_folder='templates')
client = pymongo.MongoClient(connection_url, tlsCAFile=ca)

mongo = client
# Database
Database = client.get_database('Google_App_Store_Data')
# Table
no_good_app_collection = Database.Google_App_Store_Data
good_app_collection = Database.test

@app.route("/")
def index():
   return render_template("index.html", tables = [cleaning.clean_data(no_good_app_collection).to_html(classes = 'data', header = 'true')], 
                            titles = cleaning.clean_data(no_good_app_collection).columns.values)

@app.route('/filter', methods=['GET','POST'])
def filter():
    return render_template("index.html", tables = [cleaning.clean_data2(good_app_collection).to_html(classes = 'data', header = 'true')], 
                            titles = cleaning.clean_data(good_app_collection).columns.values)

if __name__ == '__main__':
    app.run(debug=True)
