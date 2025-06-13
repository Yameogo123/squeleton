

import { useErrorToast, useWarningToast } from "@/hooks/useToast";
import { Send } from "./service";



export async function saveFile(file: any, token: string | undefined = "") {
    try {
        if (!file) {
            useWarningToast("Fournir un fichier de profil.");
            return -1;
        }
    
        const formData = new FormData();
        formData.append("file", file);

        let result: any = await Send("/file/new", formData, false, token);

        if (Object.keys(result).includes("file")) {
            return result?.file;
        }
    } catch (error) {
        useErrorToast("erreur serveur");
    }
    return -1;
}