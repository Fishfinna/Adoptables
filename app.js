
  let shelterName = document.getElementById('shelter name')
  let email = document.getElementById('email')
  let phone = document.getElementById('phone')
  let address = document.getElementById('address')
  let zip = document.getElementById('zip')
  let myInput = document.getElementById('psw')
  let repeatedPassword = document.getElementById('psw-repeat')
  let letter = document.getElementById('letter')
  let length = document.getElementById('length')
  
// When the user clicks on the password field, show the message box
myInput.onfocus = function() {
    document.getElementById("message1").style.display = "block";
  }
  
  // When the user clicks outside of the password field, hide the message box
  myInput.onblur = function() {
    document.getElementById("message1").style.display = "none";
  }
  
  // When the user starts to type something inside the password field
  myInput.onkeyup = function() {
    // Validate lowercase letters
    var lowerCaseLetters = /[a-z]/g;
    if(myInput.value.match(lowerCaseLetters)) {
      letter.classList.remove("invalid");
      letter.classList.add("valid");
    } else {
      letter.classList.remove("valid");
      letter.classList.add("invalid");
  }
  
    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if(myInput.value.match(upperCaseLetters)) {
      capital.classList.remove("invalid");
      capital.classList.add("valid");
    } 
  
    // Validate numbers
    var numbers = /[0-9]/g;
    if(myInput.value.match(numbers)) {
      number.classList.remove("invalid");
      number.classList.add("valid");
    } 
  
    // Validate length
    if(myInput.value.length >= 8) {
      length.classList.remove("invalid");
      length.classList.add("valid");
    } 
  }
    // match password
    pswConfirm = document.getElementById('psw-confirm')
    repeatedPassword.onfocus = function() {
      document.getElementById("message2").style.display = "block";
    }
    
    // When the user clicks outside of the password field, hide the message box
    repeatedPassword.onblur = function() {
      document.getElementById("message2").style.display = "none";
    }
    repeatedPassword.onkeyup = function() {
    if (repeatedPassword.value === myInput.value) {
      pswConfirm.classList.remove("invalid")
      pswConfirm.classList.add("valid")
    }
    }
