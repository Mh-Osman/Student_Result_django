document.getElementById('contactForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const contactData = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    message: document.getElementById('message').value
  };

  localStorage.setItem('contactFormData', JSON.stringify(contactData));
  alert("Your message has been saved! Thank you for contacting us.");

  // Optional: Clear the form
  this.reset();
});
