/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#f2edd5',
        fontFamily: '"Trade Winds", serif',
        // fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#f2edd5'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
// var clientSecret = $('#id_client_secret').text().slice(1, -1);
// var stripe = Stripe(stripePublicKey);

// var elements = stripe.elements();

// var style = {
//     base: {
//         color: '##f2edd5',
//         fontFamily: "Trade Winds", serif,
//         fontSmoothing: 'antialiased',
//         fontSize: '16px',
//         '::placeholder': {
//             color: '#f2edd5'
//         }
//     },
//     invalid: {
//         color: '#dc3545',
//         iconColor: '#dc3545'
//     }
// };

// var card = elements.create('card');
// card.mount('#card-element', {style: style});