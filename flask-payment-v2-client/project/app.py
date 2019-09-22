import os
import stripe

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from .paypal import GetOrder
from paypalcheckoutsdk.orders import OrdersGetRequest


# Instantiate the app
app = Flask(__name__)

api = Api(app)


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
class PaymentFrame(Resource):
    def get(self):
        return render_template('frame.html',
            key = stripe_keys['publishable_key']
        )

api.add_resource(PaymentFrame, '/payment/frame')


# Return payment script
class PaymentJs(Resource):
    def get(self):
        return send_from_directory(
            'static',
            'payment.js', 
            as_attachment = True
        )

api.add_resource(PaymentJs, '/payment/js')


# Return a HTML page to test payment
class PaymentTestPage(Resource):
    def get(self):
        return render_template('payment.html')

api.add_resource(PaymentTestPage, '/payment/test')


# Stripe test page
@app.route('/stripe')
def stripe_test():
    return render_template('stripe.html', key = stripe_keys['publishable_key'])


# Paypal test page
@app.route('/paypal')
def paypal_test():
    return render_template('paypal.html')


# Charge client
# POST request only
"""
@app.route('/charge', methods = ['POST'])
def charge():
    try:
        customer = stripe.Customer.create(
            email = 'sample@customer.com',
            source = request.json['token']
        )
        
        stripe.Charge.create(
            customer = customer.id,
            amount = request.json['amount'],
            currency = 'eur',
            description = request.json['description']
        )

        return jsonify({'status': 'Success'})

    except stripe.error.StripeError:
        return jsonify({'status': 'Error'}), 500
"""


class Charge(Resource):
    pass


class ChargeStripe(Charge):
    pass


class ChargePaypal(Charge):
    pass


@app.route('/charge_stripe', methods = ['POST'])
def charge_stripe():
    response = jsonify('Error')
    response.status_code = 500

    try:
        customer = stripe.Customer.create(
            email = request.json['email'],
            source = request.json['token']
        )
        
        stripe.Charge.create(
            customer = customer.id,
            amount = request.json['amount'],
            currency = 'eur',
            description = request.json['description']
        )

        response = jsonify('Success')
        response.status_code = 202

    except stripe.error.StripeError:
        return response

    return response


@app.route('/charge_paypal', methods = ['POST'])
def charge_paypal():
    GetOrder().get_order(request.json['order_id'])
    return jsonify({'status': 'Success'})


if __name__ == '__main__':
    app.run(debug = True)
