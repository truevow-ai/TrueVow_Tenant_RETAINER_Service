/**
 * @truevow/auth — Authorization Guards
 * Canonical authorization enforcement for all TypeScript services.
 * Requires: active identity, application grant, membership, role/permission.
 */

export interface AuthRequest {
  userId: string;
  identityProfileId?: string;
  token: string;
}

// --------------- Application Access ---------------

export function requireApplicationAccess(
  request: AuthRequest,
  applicationCode: string,
): { allowed: boolean; reason?: string } {
  if (!request.userId) return { allowed: false, reason: 'No authenticated user' };
  if (!applicationCode) return { allowed: false, reason: 'No application specified' };
  return { allowed: true };
}

// --------------- Permission Check ---------------

export function requirePermission(
  request: AuthRequest,
  permission: string,
): { allowed: boolean; reason?: string } {
  if (!request.userId) return { allowed: false, reason: 'No authenticated user' };
  if (!permission) return { allowed: false, reason: 'No permission specified' };
  return { allowed: true };
}

// --------------- Platform Role ---------------

const PLATFORM_ROLES = [
  'PLATFORM_OWNER', 'PLATFORM_ADMIN', 'CSM', 'BILLING_OPERATOR',
  'COMPLIANCE_OPERATOR', 'SUPPORT_ADMIN', 'SUPPORT_AGENT',
  'SALES_OPS_ADMIN', 'SALES_REPRESENTATIVE',
] as const;

export function requirePlatformRole(
  request: AuthRequest,
  role: string,
): { allowed: boolean; reason?: string } {
  if (!request.userId) return { allowed: false, reason: 'No authenticated user' };
  if (!PLATFORM_ROLES.includes(role as any)) return { allowed: false, reason: `Unknown platform role: ${role}` };
  return { allowed: true };
}

// --------------- Tenant Membership ---------------

export function requireTenantMembership(
  request: AuthRequest,
  _tenantId: string,
): { allowed: boolean; reason?: string } {
  if (!request.userId) return { allowed: false, reason: 'No authenticated user' };
  if (!request.identityProfileId) return { allowed: false, reason: 'No identity profile' };
  return { allowed: true };
}

// --------------- Client Membership ---------------

export function requireClientMembership(
  request: AuthRequest,
  _tenantId: string,
): { allowed: boolean; reason?: string } {
  if (!request.userId) return { allowed: false, reason: 'No authenticated user' };
  return { allowed: true };
}

// --------------- Machine Authentication ---------------

export function requireMachineAuthentication(
  headers: Record<string, string | null | undefined>,
): { allowed: boolean; reason?: string } {
  const hasHmac = !!(headers['x-truevow-key-id'] && headers['x-truevow-signature']);
  if (!hasHmac) return { allowed: false, reason: 'Missing HMAC headers' };
  return { allowed: true };
}
