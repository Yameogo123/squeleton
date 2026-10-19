import { expect, jest, test } from '@jest/globals';
import { fireEvent, render, screen } from '@testing-library/react-native';
import LoginScreen from '@/app/login';
import { SessionProvider } from '@/context/session';

jest.mock('expo-router', () => ({
  Link: ({ children }: { children: React.ReactNode }) => children,
  router: { back: jest.fn() },
  useLocalSearchParams: () => ({}),
}));

test('shows inline errors instead of calling the API with an empty form', async () => {
  const fetchSpy = jest.spyOn(globalThis, 'fetch');
  await render(
    <SessionProvider>
      <LoginScreen />
    </SessionProvider>,
  );
  await fireEvent.press(screen.getByRole('button', { name: 'Se connecter' }));
  expect(await screen.findByText('Email invalide')).toBeTruthy();
  expect(screen.getByText('Mot de passe requis')).toBeTruthy();
  expect(fetchSpy).not.toHaveBeenCalled();
});
