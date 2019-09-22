import os
import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = os.environ['PAYPAL_ID']
        self.client_secret = os.environ['PAYPAL_SECRET']

        """In production, use LiveEnvironment."""
        self.environment = SandboxEnvironment(client_id = self.client_id, client_secret = self.client_secret)

        self.client = PayPalHttpClient(self.environment)


    def object_to_json(self, json_data):
    	results = {}
    	if sys.version_info[0] < 3:
    		itr = json_data.__dict__.iteritems()

    	else:
    		itr = json_data.__dict__.items()

    	for key, value in itr:

    		if key.startswith('__'):
    			continue

    		results[key] = self.array_to_json_array(value) if isinstance(value, list) else\
    						self.object_to_json(value) if not self.is_primittive(value) else \
    						value
    	return results


    def is_primittive(self, data):
    	return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)


class GetOrder(PayPalClient):
    def get_order(self, order_id):
        request = OrdersGetRequest(order_id)

        response = self.client.execute(request)

        print ('Status Code: ', response.status_code)
        print ('Status: ', response.result.status)
        print ('Order ID: ', response.result.id)
        print ('Intent: ', response.result.intent)
        print ('Links:')
        
        for link in response.result.links:
            print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        
        print ('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                           response.result.purchase_units[0].amount.value))

