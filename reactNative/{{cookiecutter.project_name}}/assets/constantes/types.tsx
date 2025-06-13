




export type userType = {
    _id: string;
    nom: string;
    prenom: string;
    genre: string;
    tel: string;
    email: string;
    password?: string;
    birth?: string;
    nationalite?: string;
    active?: boolean;
    premium?: boolean;
    profil?: any;
};

export interface LoginResponse {
    access_token: string;
    [key: string]: any; // To allow other properties if needed
}


export type sessionType = {
    userId?: string;
    token?: string;
    expoToken?: string;
}
