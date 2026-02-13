import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCyiByyyw1xP4_J3NzwH-tMDtuZfGOuYkg",
    authDomain: "appscms-dev.firebaseapp.com",
    projectId: "appscms-dev", 
    storageBucket: "appscms-dev.firebasestorage.app",
    messagingSenderId: "731036215766",
    appId: "1:731036215766:web:e762b1747436708ebe1c77",
    measurementId: "G-DW1069865K"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app); 

export const getIdToken = async (): Promise<string | null> => {
  try {
    const token = auth.currentUser ? await auth.currentUser.getIdToken() : null;
    return token;
  } catch (error) {
    console.error("Error getting ID token:", error);
    return null;
  }
};