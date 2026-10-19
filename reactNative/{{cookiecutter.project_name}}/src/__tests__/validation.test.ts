import { expect, test } from '@jest/globals';
import { validateEmail, validatePassword, validatePhone } from '@/lib/validation';

test('validators match the backend rules', () => {
  expect(validateEmail('a@b.co')).toBeNull();
  expect(validateEmail('nope')).not.toBeNull();
  expect(validatePassword('Secret12!')).toBeNull();
  expect(validatePassword('secret12!')).toBe('Une majuscule requise');
  expect(validatePhone('')).toBeNull();
  expect(validatePhone('+226 70 00 00 00')).toBeNull();
});
