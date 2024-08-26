import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'https://www.gstatic.com/firebasejs/9.23.0/firebase-storage.js';

// Firebase configuration
const firebaseConfig = {
    apiKey: "",
    databaseURL: "https://newwhitefeather-90c13-default-rtdb.europe-west1.firebasedatabase.app",
    authDomain: "newwhitefeather-90c13.firebaseapp.com",
    projectId: "newwhitefeather-90c13",
    storageBucket: "newwhitefeather-90c13.appspot.com",
    messagingSenderId: "1961759878987",
    appId: "",
    measurementId: "G-SMEZK10E7P"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

window.uploadimage = function ()
{
    const file = document.getElementById("files").files[0];

    if (!file)
    {
        console.error("No file selected");
        return;
    }

    const storageRef = ref(storage, `images/${file.name}`);

    uploadBytes(storageRef, file, { contentType: 'image/jpg' })
        .then((snapshot) =>
        {
            console.log("Upload file successfully");
            return getDownloadURL(snapshot.ref);
        })
        .then((downloadURL) =>
        {
            console.log("Got URL:", downloadURL);
            document.getElementById("url").value = downloadURL;
            alert("File uploaded successfully");
        })
        .catch((error) =>
        {
            console.error("Upload failed:", error);
        });
};