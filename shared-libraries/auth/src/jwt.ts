/**
 * @truevow/auth — Server-Side JWT Verification
 * Canonical Supabase Auth JWT verifier for all TypeScript services.
 * Uses asymmetric JWKS — no shared signing secret needed.
 */
import { jwtVerify, createRemoteJWKSet } from 'jose';

interface AuthContext {
  sub: string;
  email: string | null;
  iss: string;
  aud: string;
  iat: number;
  exp: number;
}

let _jwksCache: ReturnType<typeof createRemoteJWKSet> | null = null;

function getJWKS(): ReturnType<typeof createRemoteJWKSet> {
  if (!_jwksCache) {
    const jwksUrl =
      process.env.SUPABASE_JWKS_URL ||
      `${process.env.NEXT_PUBLIC_SUPABASE_URL}/auth/v1/.well-known/jwks.json`;
    _jwksCache = createRemoteJWKSet(new URL(jwksUrl));
  }
  return _jwksCache;
}

function getIssuer(): string {
  return (
    process.env.SUPABASE_JWT_ISSUER ||
    `${process.env.NEXT_PUBLIC_SUPABASE_URL}/auth/v1`
  );
}

function getAudience(): string {
  return process.env.SUPABASE_JWT_AUDIENCE || 'authenticated';
}

export async function verifySupabaseJwt(token: string): Promise<AuthContext | null> {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, getJWKS(), {
      issuer: getIssuer(),
      audience: getAudience(),
    });
    return {
      sub: payload.sub!,
      email: (payload.email as string) || null,
      iss: payload.iss!,
      aud: (payload.aud as string) || '',
      iat: payload.iat as number,
      exp: payload.exp as number,
    };
  } catch {
    return null;
  }
}

export async function getAuthenticatedSubject(token: string): Promise<string | null> {
  const ctx = await verifySupabaseJwt(token);
  return ctx?.sub ?? null;
}

export function isClerkJwt(token: string): boolean {
  try {
    const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString());
    return payload.iss?.includes('clerk') || payload.azp?.includes('clerk') || false;
  } catch {
    return false;
  }
}
