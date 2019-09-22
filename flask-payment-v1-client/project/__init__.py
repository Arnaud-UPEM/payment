import os

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


# Instantiate the app
app = Flask(__name__)

api = Api(app)
CORS(app)


# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


# instantiate the db
db = SQLAlchemy(app)

from .models import *


# Check backend is up
class PaymentPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }

api.add_resource(PaymentPing, '/payment/ping')


"""
    Render our main payment page
"""
@app.route('/payment')
def payment():
    return render_template('payment.html')


"""
    Checkout interface between frontend and backend
    Frontend page send request via payment.js
    And 
"""
@app.route('/checkout', methods = ['POST'])
def checkout():
    response = jsonify('Success')
    response.status_code = 202

    # print (request.json['provider'])
    print (request.json['providerKey'])

    return response
    

if __name__ == '__main__':
    app.run(debug = True, port = 5001)
