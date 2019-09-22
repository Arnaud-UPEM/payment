import enum
import uuid
import datetime
import sqlalchemy

from . import db
from sqlalchemy.dialects.postgresql import UUID

class OrderProvider(enum.Enum):
	Stripe = 1
	PayPal = 2


class Order(db.Model):
	uuid = db.Column(UUID(as_uuid = True), unique = True, nullable = False, primary_key = True, default = str(uuid.uuid4()))
	name = db.Column(db.String(128), nullable = False)
	description = db.Column(db.String(128), default = '')

	amount = db.Column(db.Integer, nullable = False)
	currency = db.Column(db.String(128), nullable = False)

	datetime = db.Column(db.DateTime, nullable = False, default = datetime.datetime.utcnow)

	# Stripe = token
	# PayPal = orderID
	provider = db.Column(db.Enum(OrderProvider), nullable = False)
	providerKey = db.Column(db.String(128), nullable = False)

	customerID = db.Column(db.Integer, nullable = False)


	def __init__(self, name, description, amount, currency, provider, providerKey, customerID):
		self.uuid = str(uuid.uuid4())

		self.name = name
		self.description = description

		self.amount = amount
		self.currency = currency

		self.provider = provider
		self.providerKey = providerKey

		self.customerID = customerID


	def __str__(self):
		return 'name: {} with description: {}'.format(self.name, self.description)



class OrderItem:
	pass