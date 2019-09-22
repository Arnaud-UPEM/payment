console.log('payment.js');


var Payment = {

	settings: {},

	purchase_details: {
	/*
		name: '',
		description: '',
		email: '',
		amount: 0,
		items: [
			//  "name": "Fitness Watch",
		 	//  "sku": "sku04",
		 	//  "price": "0.55",
		 	//  "currency": "USD",
		 	//  "quantity": "1"
		],
	*/
	},
	

	configure: function(settings) {
		this.settings = settings;
	},


	open: function(purchase_details) {
		this.purchase_details = purchase_details;

		document.querySelector('#payment-frame').contentWindow.open();
		document.querySelector('#payment-frame').style.visibility = 'visible';
	},

	close: function() {
		document.querySelector('#payment-frame').style.visibility = 'hidden';
	},


	onSuccess: function(providerKey) {
		console.log('onSuccess');

		fetch('/payment/direct_checkout', {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify({
				
			}),
		});
	},

	onFailure: function() {
		console.log('onFailure');
	},
};


function create_iframe() {
	var iframe = document.createElement('iframe');
		iframe.id = 'payment-frame';
		iframe.src = 'http://127.0.0.1:5000/frame';
		iframe.frameBorder = '0';

		iframe.style.width = '100%';
		iframe.style.height = '100%';

		iframe.style.top = '0';
		iframe.style.left = '0';
		iframe.style.position = 'fixed';
		iframe.style.visibility = 'hidden';
		// iframe.allowtransparency = ""

	document.addEventListener('DOMContentLoaded', function() {
		document.querySelector('body').appendChild(iframe);
	}, false);
}

create_iframe();

// window.addEventListener('popstate', function() {
// 	console.log('payment-frame-close');
// }, false);