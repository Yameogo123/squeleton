import { afterEach, expect, test, vi } from 'vitest'
import { ApiError, configureApi, Get } from '@/services/service.api'

afterEach(() => vi.restoreAllMocks())

test('adds the bearer token and logs out on 401', async () => {
  const onUnauthorized = vi.fn()
  configureApi({ getToken: () => 'tok', onUnauthorized })
  const fetchMock = vi
    .spyOn(globalThis, 'fetch')
    .mockResolvedValue(new Response(JSON.stringify({ detail: 'Invalid or expired token' }), { status: 401 }))

  await expect(Get('/user/me')).rejects.toBeInstanceOf(ApiError)
  const headers = fetchMock.mock.calls[0]![1]!.headers as Headers
  expect(headers.get('Authorization')).toBe('Bearer tok')
  expect(onUnauthorized).toHaveBeenCalledOnce()
})
