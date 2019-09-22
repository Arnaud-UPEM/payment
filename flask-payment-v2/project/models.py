import enum

from . import db
from sqlalchemy.dialects.postgresql import UUID

class OrderProvider(enum.Enum):
	Stripe = 1
	PayPal = 2


class Order(db.Model):
	uuid = db.Column(UUID(as_uuid = True), unique = True, nullable = False, primary_key = True)
	name = db.Column(db.String(128), nullable = False)
	description = db.Column(db.String(128), default = '')
	amount = db.Column(db.Integer(), nullable = False)
	provider = db.Column(db.Enum(OrderProvider), nullable = False)

	# Stripe = token
	# PayPal = orderID
	providerKey = db.Column(db.String(128), nullable = False)

	currency = db.Column(db.String(128), nullable = False)
	customerEmail = db.Column(db.String(128), nullable = False)

	def __str__(self):
		return 'name: {} with description: {}'.format(name, description)

	pass


class OrderItem:
	pass