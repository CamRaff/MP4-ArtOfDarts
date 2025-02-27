# CamRaff - Milestone Project 4 - Art of Darts

![displays](readme_images/amiresponsive-displays.png)

Here is a link to my deployed site: [Art of Darts](https://art-of-darts-mp4-13da8fbba8de.herokuapp.com/)

---

# Contents

- [Automated Testing](#automated-testing)

    - [W3C HTML Validator](#w3c-html-validator)

    - [CSS Jigsaw](#css-jigsaw)

    - [JS Hint](#js-hint)

---

# Automated Testing

## W3C HTML Validator

To test all of the HTML pages on this site, I used the [W3C HTML Validator](https://validator.w3.org/). All pages flagged an error due to the mobile-top-header.html and main-nav.html both being included in the page using Django syntax, with only 1 of them actually being visible depending on the size of the screen you're using. Each page that contained Javascript also had a warning due to me including 'type="text/javascript"' as apparently the type attribute isn't necessary for Javascript resources.

### Home Page

<img src="readme_images/w3c-html/home.png" height="300">

### All Products Page

This page had several warnings about the potential mis-use of aria-labels, however, I believe these are necessary as they provide information about the options in the list.

<img src="readme_images/w3c-html/all-products.png" height="300">

### Product Details Page

<img src="readme_images/w3c-html/product-details.png" height="300">

### View Bag Page

<img src="readme_images/w3c-html/bag.png" height="300">


### Checkout Page

This page produced a warning due to the use of a h1 element to utilize the Font Awesome icon used as the loading spinner. As there was no text, it classed this element as being empty.

<img src="readme_images/w3c-html/checkout.png" height="300">

### Checkout Success Page

<img src="readme_images/w3c-html/checkout-success.png" height="300">

### Profile Page

<img src="readme_images/w3c-html/profile.png" height="300">

### Add Product Page

This page had a duplicate attribute error due to me setting an ID to allow for Javascript to function, while the Django Widget also added an ID to the same element. I was unable to get the functionality the same while using the Django Widget ID, so I opted to allow this error.

<img src="readme_images/w3c-html/add-product.png" height="300">

### Edit Product Page

As this page utilized the same Django Widget, it produced the same error as above. 

<img src="readme_images/w3c-html/edit-product.png" height="300">

## CSS Jigsaw

To test the CSS files used for this site, I used [CSS Jigsaw](https://jigsaw.w3.org/css-validator/). The results for each file were as follows:

### base.css

<img src="readme_images/css-jigsaw/jigsaw-base.png" height="200">

### profiles.css

<img src="readme_images/css-jigsaw/jigsaw-profiles.png" height="200">

### checkout.css

<img src="readme_images/css-jigsaw/jigsaw-checkout.png" height="200">

## JS Hint

To test the JavaScript file used in the site, I used [JSHint](https://jshint.com/). The test results were as follows:

<img src="readme_images/js-hint.png" height="300">