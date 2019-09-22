import os

from flask import Flask, jsonify, render_template, request, abort

# Instantiate the app
app = Flask(__name__)


products = [
    {
        'id': 1,
        'name': 'Something Special',
        'description': 'Something really, really special',
        'amount': 600
    },
    {
        'id': 2,
        'name': 'More Special',
        'description': 'Something even more special',
        'amount': 700
    },
]

def get_product(id):
	for p in products:
		if p['id'] == id:
			return p
	return False


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/products/<int:product_id>')
def product(product_id):
	p = get_product(product_id)
	if (p):
		p['amount_in_eur'] = p['amount'] / 100
		return render_template('product.html', p = p)
	else:
		return abort(404)


@app.route('/charge', methods = ['POST'])
def charge():
	pass


@app.route('/ping')
def ping():
	return jsonify({'status': 'success', 'message': 'pong!'})


if __name__ == '__main__':
	app.run(debug = True, port = 5001)
