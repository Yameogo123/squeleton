import { toast } from "react-toastify";
//import { Remove, Send, Update, Get } from "../services/service.api";
import { Send } from "../services/service.api";
//import { getCurrentDate, isEmail, isName, isPassword, isPhone } from "./controller.utils";



/**
 * Handles the login process.
 *
 * @param {Event} e - The event object.
 * @param {string} email - The email address of the user.
 * @param {string} password - The password of the user.
 * @returns {Promise<{type: string, value: {user: Object, token: string}}|number>} 
 *          Returns an object with user and token if login is successful, otherwise returns -1.
 */
export async function handleLogin(e, email, password) {
    e.preventDefault();
    if (email === "" || password === "") {
        toast.error("Veuillez remplir tous les champs");
    }else{
        let data = {
            email: email,
            password: password
        }
        try {
            let result = await Send("/login", data);
            if (Object.keys(result).length !== 0) {
                toast.success("Connexion réussie");
                return { type: "login", value: { "user": result, "token": result?.access_token} }
            }else{
                toast.error("Email ou mot de passe incorrect");
            }
        } catch (error) {
            toast.error("erreur lors de la connexion");
        }
    }
    return -1;
}