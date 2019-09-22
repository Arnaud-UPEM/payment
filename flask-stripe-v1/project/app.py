import os
import stripe

from flask import Flask, jsonify, render_template, request, send_from_directory

# Instantiate the app
app = Flask(__name__)

stripe_keys = {
	'secret_key': os.environ['STRIPE_SECRET_KEY'],
  	'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


@app.route('/')
def index():
	return render_template('index.html', key = stripe_keys['publishable_key'])


@app.route('/frame')
def frame():
	return render_template('frame.html')


@app.route('/payment.js')
def paymentjs():
	return send_from_directory('static', 'payment.js', as_attachment = True)


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


@app.route('/charge_stripe', methods = ['POST'])
def charge_stripe():
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


@app.route('/ping')
def ping():
	return jsonify({'status': 'success', 'message': 'pong!'})


if __name__ == '__main__':
	app.run(debug = True)
