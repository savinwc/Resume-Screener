const firebaseConfig = {
  apiKey: "AIzaSyCICSIvYgI0Z1-7kiC1_h_gnhOV20fQEi4",
  authDomain: "employeesignup-c9150.firebaseapp.com",
  databaseURL: "https://employeesignup-c9150-default-rtdb.firebaseio.com",
  projectId: "employeesignup-c9150",
  storageBucket: "employeesignup-c9150.appspot.com",
  messagingSenderId: "218012313836",
  appId: "1:218012313836:web:9c9a83b7391cf737a6ddc9"
};

// initialize firebase
firebase.initializeApp(firebaseConfig);

var storageRef = firebase.storage().ref();
// reference your database
var contactFormDB = firebase.database().ref("contactForm");

document.getElementById("contactForm").addEventListener("submit", submitForm);

function uploadImage() {
  const ref = firebase.storage().ref();
  const file = document.querySelector("#photo").files[0];
  const name = +new Date() + "-" + file.name;
  const metadata = {
     contentType: file.type
  };
  const task = ref.child(name).put(file, metadata);task
  .then(snapshot => snapshot.ref.getDownloadURL())
  .then(url => {
  console.log(url);
  alert('Resume Uploaded Successfully');
  document.querySelector("#image").src = url;
})
.catch(console.error);
}
const errorMsgElement = document.querySelector('span#errorMsg');


function submitForm(e) {
  e.preventDefault();

  var EmployeeName = getElementVal("EmployeeName");
  var EmployeeEmailID = getElementVal("EmployeeEmailID");
  var EmployeePhoneNO = getElementVal("EmployeePhoneNO");
  var EmployeePosition = getElementVal("EmployeePosition")
  var Employee_StartDate= getElementVal("Employee_StartDate")
  var Current_Employee_Status=getElementVal("Current_Employee_Status")
  var Password = getElementVal("Password");
  
  
  saveMessages(EmployeeName,EmployeeEmailID,EmployeePhoneNO,EmployeePosition,Employee_StartDate,Current_Employee_Status,Password);

  //   enable alert
  document.querySelector(".alert").style.display = "block";

  //   remove the alert
  setTimeout(() => {
    document.querySelector(".alert").style.display = "none";
  }, 3000);

  //   reset the form
  document.getElementById("contactForm").reset();
}

const saveMessages = (EmployeeName,EmployeeEmailID,EmployeePhoneNO,EmployeePosition,Employee_StartDate,Current_Employee_Status,Password) => {
  var newcontactForm = contactFormDB.push();

  newcontactForm.set({
    EmployeeName:EmployeeName,
    EmployeeEmailID:EmployeeEmailID,
    EmployeePhoneNO:EmployeePhoneNO,
    EmployeePosition:EmployeePosition,
    Employee_StartDate:Employee_StartDate,
    Current_Employee_Status:Current_Employee_Status,
    Password:Password
    
  });
};

const getElementVal = (id) => {
  return document.getElementById(id).value;
};


