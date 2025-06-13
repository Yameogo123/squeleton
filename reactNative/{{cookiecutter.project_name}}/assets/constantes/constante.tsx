import { Platform } from "react-native";


export const API_URL = Platform.select({
    android: 'http://127.0.0.1:8000',
    ios: 'http://192.168.1.199:8000',
    default: 'http://localhost:8000'
});



export const font = require('../fonts/SpaceMono-Regular.ttf');


export const bgcol = "#FFF"; // Background color
export const app_color = "#6A52ED"; 
export const transparent = "transparent";
export const white = "snow"; // White color

export const images = [
    "https://static.vecteezy.com/ti/vecteur-libre/p1/8169402-formes-abstraites-et-lignes-dans-les-couleurs-pastel-nudes-fond-neutre-dans-le-style-minimaliste-contemporain-illustrationle-gratuit-vectoriel.jpg",
    "https://img.freepik.com/vecteurs-premium/modele-fond-motif-couleur-neutre_656853-281.jpg",
    "https://img.freepik.com/vecteurs-premium/fond-illustration-dessine-main-formes-abstraites-illustration-vectorielle_656853-671.jpg"
]