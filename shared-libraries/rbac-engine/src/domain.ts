/**
 * Service Domain Enum
 *
 * Defines the three trust domains in the TrueVow platform.
 * Previously imported from @truevow/auth-client — now self-contained
 * in rbac-engine to eliminate the @clerk/nextjs transitive dependency.
 *
 * The legacy name "ClerkDomain" is preserved for backward compatibility
 * with all existing code that imports it.
 */
export enum ClerkDomain {
  PLATFORM_OPERATORS = 'PLATFORM_OPERATORS',
  SALES_SUPPORT = 'SALES_SUPPORT',
  TENANTS = 'TENANTS',
}
