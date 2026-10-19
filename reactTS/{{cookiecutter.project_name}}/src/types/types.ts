export type Role = 'user' | 'admin'

export interface User {
  _id: string
  nom: string
  prenom: string
  email: string
  tel?: string
  adresse?: string
  role: Role
  actif?: boolean
  profil?: string
}

/** POST /user/login response: the user + the token */
export interface LoginResponse extends User {
  access_token: string
  token_type: 'Bearer'
  expires_in: number
}

export interface ApiMessage {
  message: string
  state: 'success' | 'warning' | 'error'
}
