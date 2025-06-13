
import { useErrorToast, useSuccessToast, useWarningToast } from "@/hooks/useToast";
import { LoginResponse } from "@/assets/constantes/types";
import { isEmail, isPhone } from "./controller.utils";
import { Get, Send, Update } from "./service";




export async function handleLogin(email: string, password: string): Promise<{ type: string; value: { user: LoginResponse; token: string; }; } | number> {
    if (email === "" || password === "") {
        useWarningToast('Veuillez remplir tous les champs.');
    } else {
        let data = {
            "email": email,
            "password": password
        };
        try {
            let result = await Send("/login", data) as LoginResponse;

            if (result.access_token) {
                useSuccessToast("Connexion réussie");
                return { type: "login", value: { "user": result, "token": result.access_token } };
            } else {
                useWarningToast("Email ou mot de passe incorrect");
            }
        } catch (error) {
            useErrorToast("erreur lors de la connexion");
        }
    }
    return -1;
}

export async function getUser(id: string, token: string = ""){
    if(id!==""){
        try {

            let res = await Get("/user/"+id, token);

            if (Object.keys(res).includes("user")) {
                return (res as { user: object })['user'];
            }
        } catch (error) {
            
            useErrorToast("erreur lors de la connexion");
        }
    }
    return {}
}


export async function insertUser(
    nom: string,
    prenom: string,
    tel: string,
    email: string,
    password: string,
    birth: string,
    nationalite: string,
): Promise<any> {
    if (!nom || !prenom) {
        useWarningToast("Les nom et prénom sont obligatoires.");
        return -1;
    }

    if(!isPhone(tel)){
        useWarningToast("Un bon format de téléphone est obligatoire.");
        return -1;
    }

    if(email && !isEmail(email)){
        useWarningToast("Un bon format de mail est obligatoire.");
        return -1;
    }


    let data = {
        nom: nom, prenom: prenom, tel: tel, email: email,
        password: password, nationalite: nationalite, birth: birth
    };


    try { 
        let result = await Send("/signin", data, true);

        if (Object.keys(result).includes("message")) {
            useSuccessToast("Votre compte a été créé avec succès");
            return 1
        } else {
            useWarningToast("Échec de l'ajout de l'utilisateur.");
        }
    } catch (error) {
        useErrorToast("Erreur serveur.");
    }

    return -1;
}


export async function updateUser(
    id: string,
    nom: string,
    prenom: string,
    genre: string,
    birth: string,
    tel: string,
    email: string,
    token: string,
    
): Promise<any> {
    
    if (!nom || !prenom) {
        useWarningToast("Les nom et prénom sont obligatoires.");
        return -1;
    }

    if (!id) {
        useWarningToast("Fournir votre id.");
        return -1;
    }

    if(email && !isEmail(email)){
        useWarningToast("Un bon format de mail est obligatoire.");
        return -1;
    }

    if(!isPhone(tel)){
        useWarningToast("Un bon format de téléphone est obligatoire.");
        return -1;
    }

    let data = {
        nom: nom, prenom: prenom, genre: genre, birth: birth, active: true,
        tel: tel, email: email
    };    

    try {
        let result = await Update("/user/"+id, data, token);
        
        if (Object.keys(result).includes("message")) {
            useSuccessToast("Votre compte a été mis à jour avec succès");
            return 1;
        } else {
            useWarningToast("Échec de mise à jour.");
        }
    } catch (error) {
        useErrorToast("Erreur serveur.");
    }
 
    return -1;
}



export async function updateUserPassword(
    id?: string,
    oldpass?: string,
    newpass?: string,
    token?: string,
    
): Promise<any> {
    
    if (!oldpass || !newpass) {
        useWarningToast("Les nom et prénom sont obligatoires.");
        return -1;
    }

    if (!id) {
        useWarningToast("Fournir votre id.");
        return -1;
    }

    if(oldpass === newpass){
        useWarningToast("Le nouveau mot de passe doit être différent de l'ancien.");
        return -1;
    }

    try {
        let result = await Update("/user/"+id+"/"+oldpass+"/"+newpass, {}, token);
        
        if (Object.keys(result).includes("message")) {
            useSuccessToast("Mot de passe mis à jour");
            return 1;
        } else {
            useWarningToast("Échec de mise à jour.");
        }
    } catch (error) {
        useErrorToast("Erreur serveur.");
    }
 
    return -1;
}



export async function updateProfilePhoto(
    id: string,
    photo: any,
    token: string
): Promise<any> {
    if (!id) {
        useWarningToast("Fournir votre id.");
        return -1;
    }

    if (!photo) {
        useWarningToast("Fournir une photo de profil.");
        return -1;
    }

    const formData = new FormData();
    formData.append("file", photo);

    try {
        let result = await Update(`/set/profile/${id}`, formData, token, false);

        if (Object.keys(result).includes("message")) {
            useSuccessToast("Votre photo de profil a été mise à jour avec succès");
            return 1;
        } else {
            useWarningToast("Échec de mise à jour de la photo de profil.");
        }
    } catch (error) {
        useErrorToast("Erreur serveur.");
    }

    return -1;
}




export async function updateUserPremium(
    id?: string,
    isPremium?: number,
    token?: string
): Promise<any> {
    if (!id) {
        useWarningToast("Fournir votre id.");
        return -1;
    }

    try {
        let result = await Update(`/user/${id}/${isPremium}`, {}, token);

        if (Object.keys(result).includes("message")) {
            useSuccessToast("Statut premium mis à jour avec succès");
            return 1;
        } else {
            useWarningToast("Échec de mise à jour du statut premium.");
        }
    } catch (error) {
        useErrorToast("Erreur serveur.");
    }

    return -1;
}

