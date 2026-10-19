/** Auth endpoints of the FastAPI template (/user/...). */
import { api } from './api';

export type User = {
  _id: string;
  nom: string;
  prenom: string;
  email: string;
  tel?: string;
  role: 'user' | 'admin';
};

type LoginResponse = User & { access_token: string; token_type: 'Bearer'; expires_in: number };

export type Session = { token: string; expiresAt: number; user: User };

export type SignupInput = { nom: string; prenom: string; email: string; password: string; tel?: string };

export async function login(email: string, password: string): Promise<Session> {
  const { access_token, expires_in, token_type: _type, ...user } = await api.post<LoginResponse>('/user/login', {
    email: email.trim(),
    password,
  });
  return { token: access_token, expiresAt: Date.now() + expires_in * 1000, user };
}

export async function signup(input: SignupInput): Promise<void> {
  await api.post('/user/signin', { ...input, email: input.email.trim() });
}

export async function fetchMe(): Promise<User> {
  return (await api.get<{ user: User }>('/user/me')).user;
}
