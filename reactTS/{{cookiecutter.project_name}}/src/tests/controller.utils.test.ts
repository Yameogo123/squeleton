import { isEmail, isPassword, isPhone } from '@/controllers/controller.utils'

test('validators', () => {
  expect(isEmail('a@b.co')).toBe(true)
  expect(isEmail('nope')).toBe(false)
  expect(isPhone('+221 77 123 45 67')).toBe(true)
  expect(isPassword('Secret12!')).toBe(true)
  expect(isPassword('secret')).toBe(false)
})
