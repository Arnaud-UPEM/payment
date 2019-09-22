console.log('payment.js');


/*
	Entry point: configure()

	Trigger iframe with: open()
*/
var Payment = {

	settings: {
	/*
		onSuccess: function(providerKey) {},

		onFailure: function() {},
	*/
	},


	configure: function(settings) {
		this.settings = settings;

		this.events();
	},


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
	


	open: function(purchase_details) {
		this.purchase_details = purchase_details;


		// Blocked by browser security
		// document.querySelector('#payment-frame').contentWindow.Frame.open();

		document.querySelector('#payment-frame')
				.contentWindow.postMessage({
					name: 'frame-details',
					parameters: [
						purchase_details,
					]
				}, '*');

		document.querySelector('#payment-frame')
				.contentWindow.postMessage({
					name: 'frame-open',
					parameters: []
				}, '*');


		document.querySelector('#payment-frame').style.visibility = 'visible';
	},

	close: function() {
		document.querySelector('#payment-frame').style.visibility = 'hidden';
	},

	events: function() {

		window.addEventListener('message', function(e) {

			if (event.origin.startsWith('http://127.0.0.1')) { 

				if (typeof event.data === 'object') {

					if (event.data.name !== undefined) {

						switch (event.data.name) {

							case 'payment-close':
								Payment.close();
								break;


							case 'payment-onsuccess':
								Payment.settings.onSuccess(event.data.parameters[0]);
								break;

							case 'payment-onfailure':
								Payment.settings.onFailure(event.data.parameters[0]);
								break;


							default:
								console.log(`Payment.events() - Unknow event data: ${event.data}`);
								break;
						}
					}
				}
			}
			else {
				//
			}
		});
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