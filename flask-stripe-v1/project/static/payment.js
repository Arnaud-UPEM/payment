console.log('payment.js');

class Payment {
	constructor() {

	}

	static configure() {

		return new Payment();
	}

	open() {
		this.iframe.style.visibility = 'visible';
	}

	close() {
		this.iframe.style.visibility = 'hidden';
	}

	iframe() {
		this.iframe = document.createElement('iframe');
		this.iframe.src = 'http://127.0.0.1:5000/frame';
		this.iframe.frameBorder = "0";
		this.iframe.style.visibility = 'hidden';
		// iframe.allowtransparency = ""

		var body = document.querySelector('body');
			body.appendChild(this.iframe)
	}
}