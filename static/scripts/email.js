  emailjs.init('a63cmeaYzdunaASgN')
  var sent = false

  function sendEmail(params) {
      if (sent == false) {
          var template = {
              to_address: document.getElementById('shelter_email').innerHTML.slice(7),
              subject: document.getElementById('Subject').value,
              sender_address: document.getElementById('Email').value,
              shelter_name: document.getElementById('name-of-shelter').innerHTML.slice(14),
              pet_name: document.getElementById('pet-title').innerHTML.slice(18),
              message: document.getElementById('message').value,
              reply_to: document.getElementById('Email').value
          };
          console.log(template)
          emailjs.send("service_dd8hbe2", "template_dk8m9nd", template)
          sent = true

      }

  }