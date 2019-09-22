/*
	Problems in
		fn onError
			error is still undefined
*/
var Frame = {

	is_iframe: false,

	/*
		Most Important fn
		Its role is to communicate with its parent
	*/
	init: function() {

		window.addEventListener('message', function(e) {

			if (event.origin.startsWith('http://127.0.0.1')) { 

				if (typeof event.data === 'object') {

					if (event.data.name !== undefined) {

						switch (event.data.name) {

							case 'frame-open':
								// Frame.open(iframe, test);
								Frame.open(true, false);
								break;


							case 'frame-details':
								Frame.frame_settings = event.data.parameters[0];
								break;


							default:
								console.log(`Frame.events() - Unknow event data: ${event.data}`);
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

	// self: this,

	stripe_key: undefined,

	frame_settings: {
	/*
		name: '',
		email: '',
		description: '',

		amount: 0,
		currency: 'EUR',

		items: [
			//  "name": "Fitness Watch",
		 	//  "sku": "sku04",
		 	//  "price": "0.55",
		 	//  "currency": "USD",
		 	//  "quantity": "1"
		],
	*/
	},


	/*
		Called every time the iframe is opened
		@params
			test - Boolean - enable test mode for non-iframe mode

		@notes
			Amount is required to continue
			If not set app will close
	*/
	open: function(iframe = false, test = true) {
		console.log('iframe open');

		this.is_iframe = iframe;

		if (!this.is_iframe) {
			console.log('This window is not an iframe');

			if (test) {
				console.log('Test mode enable');

				this.frame_settings.name = 'ALSH&PERI';
				this.frame_settings.email = 'parent@mail.fr';
				this.frame_settings.description = 'Paiment ALSH/PERI 2019-2020';
				
				this.frame_settings.amount = 57050; // in cents
				this.frame_settings.currency = 'EUR';
				
				this.frame_settings.items = [
					{
						'name': 'PERI Septembre',
					 	'sku': 'peri_09_2019_2020',
					 	'price': '20.00',
					 	'currency': 'USD',
					 	'quantity': '1'
					},
					{
						'name': 'PERI Octobre',
					 	'sku': 'peri_10_2019_2020',
					 	'price': '20.00',
					 	'currency': 'USD',
					 	'quantity': '1'
					},
					{
						'name': 'PERI Novembre',
					 	'sku': 'peri_11_2019_2020',
					 	'price': '20.00',
					 	'currency': 'USD',
					 	'quantity': '1'
					},
					{
						'name': 'ASLH Mercredi',
					 	'sku': 'alsh_merc_2019_2020',
					 	'price': '17.00',
					 	'currency': 'USD',
					 	'quantity': '20'
					},
					{
						'name': 'ASLH Toussain',
					 	'sku': 'alsh_tous_2019_2020',
					 	'price': '17.00',
					 	'currency': 'USD',
					 	'quantity': '10'
					},
				];
			}
			else {
				console.log('Abort');
				return;
			}
		}
		else {
			// frame_settings is supposed to be set
			const p = this.frame_settings;
			
			// Required values
			if (p.amount === undefined) {
				console.log('Error - No amount given');
				return;
			}
			this.frame_settings.amount = p.amount;


			this.frame_settings.name = 
				(p.name !== undefined) ? p.name : '';

			this.frame_settings.email = 
				(p.email !== undefined) ? p.email : '';

			this.frame_settings.items = 
				(p.items !== undefined) ? p.items : [];

			this.frame_settings.currency = 
				(p.currency !== undefined) ? p.currency : 'EUR';

			this.frame_settings.description = 
				(p.description !== undefined) ? p.description : '';
		}

		// function open_treat_value(value, type) {

		// }

		this.UI.open();
		this.UI.events();

		this.Stripe.init();
		this.PayPal.init();
	},


	UI: {

		/*
			Fill our window with customer details
		*/
		open: function() {
			var amount = Frame.frame_settings.amount / 100;

			document.querySelector('.modal-card-title-main')
					.innerHTML = Frame.frame_settings.name;

			document.querySelector('.modal-card-title-sub small')
					.innerHTML = Frame.frame_settings.description;

			document.querySelector('.customer-email')
					.innerHTML = Frame.frame_settings.email;

			document.querySelector('.customer-amount')
					.innerHTML = amount;
					
			document.querySelector('.customer-currency')
					.innerHTML = Frame.frame_settings.currency;
		},


		/*
			Set up our window events
				Stripe buttons (open and close)
				Close buttons (top and bottom)
		*/
		events: function() {
			/*
				Stripe
			*/
			// Toggle - Open
			document.querySelector('#stripe-toggle')
				.addEventListener('click', function() {
					Frame.Stripe.open();
			});

			// Signal - Close
			window.addEventListener('popstate', function() {
				console.log('popstate');
				Frame.Stripe.close();
			});


			/*
				Modal
			*/
			// Head trigger
			document.querySelector('.delete').addEventListener('click', function() {
				Frame.UI.close();
			});
			// Cancel button
			document.querySelector('.button.is-danger').addEventListener('click', function() {
				Frame.UI.close();
			});
		},


		/*
			Close modal
		*/
		close: function() {
			if (Frame.is_iframe) {

				// parent.Payment.close();
				parent.postMessage({
					name: 'payment-close',
					parameters: []
				}, '*');
			}
			else {
				console.log('UI.close() - Can\'t close a non iframe window');
			}
		},
	},


	Common: {

		/*
			Fetch - AJAX helper
		*/
		fetch: function(provider, data) {

			var url = '';

			var body_raw = {
				name: 			Frame.frame_settings.name,
				description: 	Frame.frame_settings.description,

				amount: 		Frame.frame_settings.amount,
				currency: 		Frame.frame_settings.currency,

				customerID: 	0,
			};


			switch (provider) {
				case 'stripe':
					url = '/charge_stripe';

            		body_raw.email 			= data.email;
            		body_raw.providerKey 	= data.id;
					break;

				case 'paypal':
					url = '/charge_paypal';

            		body_raw.providerKey 	= data.orderID;
					break;

				default:
					console.log(`fetch() - Error, ${provider} is not a valid provider`);
					return;
			}


			return fetch(url, {
	                method: 'POST',
	                headers: {'Content-Type': 'application/json'},
	                body: JSON.stringify(body_raw)
	            })
	            .then(function(response) {
	                console.log(response);

	                if (response.ok) {

	                	return response.json();
	                }
	                else {
	                	if (response.status == 500) {
	                		Frame.Common.checkout_failure(provider, response.statusText);
	                	}
	                }
	            })
	            .then(function(jsonResponse) {
	            	Frame.Common.checkout_success(provider, jsonResponse.orderID);
	            });
		},


		/*
			Called when provider return a positive answer
			to a payment 
		*/
		checkout_success: function(provider, orderID) {

			switch (provider) {

				case 'stripe':
					console.log('checkout_success() - Stripe, ', orderID);
					break;

				case 'paypal':
					console.log('checkout_success() - Paypal, ', orderID);
					break;

				default:
					console.log('checkout_success() - Error, incorrect provider');
					break
			}

			if (Frame.is_iframe)
				// parent.Paypal.settings.onSuccess(orderID);
				parent.postMessage({
					name: 'payment-onsuccess',
					parameters: [
						orderID
					]
				}, '*');
		},

		/*
			Called when provider return an error 
			due to a failed payment 
		*/
		checkout_failure: function(provider, error) {

			switch (provider) {

				case 'stripe':
					console.log('checkout_failure() - Stripe, ', error);
					break;

				case 'paypal':
					console.log('checkout_failure() - Paypal, ', error);
					break;

				default:
					console.log('checkout_failure() - Error, incorrect provider');
					break
			}

			if (Frame.is_iframe) {
				// parent.Paypal.settings.onFailure(error);
				parent.postMessage({
					name: 'payment-onfailure',
					parameters: [
						error
					]
				}, '*');
			}

		},
	},


	Stripe: {

		stripe_handler: undefined,


		init: function() {			
			this.stripe_handler = StripeCheckout.configure({
	            key: Frame.stripe_key,
	            image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
	            locale: 'auto',
	            token: function(token) {
	                
	                // console.log(`Stripe token:`);
	                // console.log(token);

	                Frame.Common.fetch('stripe', token);	                
	            }
	    	});

	    	console.log('Stripe ready');
		},


		/*
			Open Stripe modal
			Triggered by our button
		*/
		open: function() {
			this.stripe_handler.open({
	            name: 			Frame.frame_settings.name,
	            email: 			Frame.frame_settings.email,
	            description: 	Frame.frame_settings.description,

	            amount: 		Frame.frame_settings.amount,
	        });
		},


		close: function() {
			this.stripe_handler.close();
		}
	},


	PayPal: {

		init: function() {

			paypal.Buttons({
				createOrder: function(data, actions) {

					const amount = 
						(Frame.frame_settings.amount / 100)
						.toString();

					return actions.order.create({
						purchase_units: [{
							amount: {
								value: amount,
								// currency_code: 'EUR',
							},
						}]
					});
				},
				onApprove: function(data, actions) {
					return actions.order.capture().then(function(details) {

						console.log('PayPal Success');

						return Frame.Common.fetch('paypal', data)
			                .then(function(details) {
			                	if (details.error === 'INSTRUMENT_DECLINED') {
							        return actions.restart();
							    }
			                });
			        });
				},
				onError: function(error) {
					if (error !== undefined) {

						console.log('PayPal Error: ', error);

						Frame.Common.checkout_failure('paypal', error);
					}
				},

			}).render('#paypal-wrapper');

			console.log('PayPal ready');
		}
	},
};