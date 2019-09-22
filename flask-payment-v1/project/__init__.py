import os
import stripe

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from .paypal import GetOrder

from datetime import datetime


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


# instantiate stripe
stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


# Check backend is up
class PaymentPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }

api.add_resource(PaymentPing, '/payment/ping')


# Return payment iframe
@app.route('/frame')
def frame():
    return render_template('frame.html', key = stripe_keys['publishable_key'])


# Serve Payment Script
@app.route('/payment.js')
def paymentjs():
    return send_from_directory('static', 'payment.js', as_attachment = True)


"""
    Save a given order in out database
"""
def charge(json, orderProvider):
    order = Order(json['name'], json['description'], json['amount'], json['currency'], orderProvider, json['providerKey'], 0)
    db.session.add(order)
    db.session.commit()
    return order.uuid
    

@app.route('/charge_stripe', methods = ['POST'])
def charge_stripe():
    try:
        customer = stripe.Customer.create(
            email = request.json['email'],
            source = request.json['providerKey']
        )
        
        stripe.Charge.create(
            customer = customer.id,
            amount = request.json['amount'],
            currency = 'eur',
            description = request.json['description']
        )

        orderID = charge(request.json, OrderProvider.Stripe)

    except stripe.error.StripeError:
        response = jsonify(status = 'Error')
        response.status_code = 500
        return response

    response = jsonify(status = 'Success', orderID = orderID)
    response.status_code = 202
    return response


@app.route('/charge_paypal', methods = ['POST'])
def charge_paypal():
    GetOrder().get_order(request.json['providerKey'])

    orderID = charge(request.json, OrderProvider.PayPal)

    response = jsonify(status = 'Success', orderID = orderID)
    response.status_code = 202

    return response




"""
    TEST FUNCTIONS
"""

# Return a HTML page to test payment
@app.route('/test_payment')
def payment_test():
    return render_template('payment.html')


# Stripe test page
@app.route('/stripe')
def stripe_test():
    return render_template('stripe.html', key = stripe_keys['publishable_key'])


# Paypal test page
@app.route('/paypal')
def paypal_test():
    return render_template('paypal.html')


@app.route('/payment/test_uuid')
def test_uuid():
    order = Order('ALSH&PERI', 'Something...', 57000, 'EUR', OrderProvider.PayPal, '22df4d5f4', 1)
    db.session.add(order)
    db.session.commit()
    return {'response': 'Ok'}



@app.route('/jsonresponse')
def jsonresponse():
    return render_template('jsonResponse.html')


@app.route('/jsonresponse_ajax', methods = ['POST'])
def jsonresponse_ajax():
    response = jsonify(status = 'Success', orderID = 58)
    response.status_code = 202
    return response 


if __name__ == '__main__':
    app.run(debug = True)
