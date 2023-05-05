const firebaseConfig = {
  apiKey: "AIzaSyCPcLcUXnjE872WlXvx7paG-lrNwIkHXFo",
  authDomain: "employersignup-cd432.firebaseapp.com",
  projectId: "employersignup-cd432",
  storageBucket: "employersignup-cd432.appspot.com",
  messagingSenderId: "203735891138",
  appId: "1:203735891138:web:fe7e640e4564907e168f5b"
};

// initialize firebase
firebase.initializeApp(firebaseConfig);

// reference your database
var contactFormDB = firebase.database().ref("contactForm");

document.getElementById("contactForm").addEventListener("submit", submitForm);

function submitForm(e) {
  e.preventDefault();

  var CompanyName = getElementVal("CompanyName");
  var CompanyAddress = getElementVal("CompanyAddress");
  var PositionRequired = getElementVal("PositionRequired");
  var EmployerName = getElementVal("EmployerName");
  var Employer_DOB = getElementVal("Employer_DOB");
  var Employer_Email_ID = getElementVal("Employer_Email_ID");
  var Employer_Position = getElementVal("Employer_Position");
  var Password = getElementVal("Password");

  saveMessages(CompanyName, CompanyAddress, PositionRequired, EmployerName, Employer_DOB, Employer_Email_ID, Employer_Position,Password);

  //   enable alert
  document.querySelector(".alert").style.display = "block";

  //   remove the alert
  setTimeout(() => {
    document.querySelector(".alert").style.display = "none";
  }, 3000);

  //   reset the form
  document.getElementById("contactForm").reset();
}

const saveMessages = (CompanyName,CompanyAddress,PositionRequired,EmployerName,Employer_DOB,Employer_Email_ID,Employer_Position,Password) => {
  var newContactForm = contactFormDB.push();

  newContactForm.set({
    CompanyName:CompanyName,
    CompanyAddress:CompanyAddress,
    PositionRequired:PositionRequired,
    EmployerName:EmployerName,
    Employer_DOB:Employer_DOB,
    Employer_Email_ID:Employer_Email_ID,
    Employer_Position:Employer_Position,
    Password:Password
  });
};

const getElementVal = (id) => {
  return document.getElementById(id).value;
};