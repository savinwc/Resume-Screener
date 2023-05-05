var firebaseConfig = {
    apiKey: "AIzaSyC5JZpHq3C1eVNnMx1JCayleFiqy2p6kOM",
    authDomain: "contactform-4509a.firebaseapp.com",
    databaseURL: "https://contactform-4509a-default-rtdb.firebaseio.com",
    projectId: "contactform-4509a",
    storageBucket: "contactform-4509a.appspot.com",
    messagingSenderId: "217610516242",
    appId: "1:217610516242:web:e2ba49ad47999bb4ea25cb"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  // Initialize variables
  const auth = firebase.auth()
  const database = firebase.database()