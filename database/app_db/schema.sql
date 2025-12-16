-- Marketing IQ Application Database Schema
-- Supabase / Local Postgres

-- =============================================================================
-- TENANT MANAGEMENT
-- =============================================================================

CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    subdomain TEXT UNIQUE,
    subscription_tier TEXT DEFAULT 'free',
    status TEXT DEFAULT 'trial',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tenant_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    role TEXT DEFAULT 'user',
    auth_user_id TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tenant_oauth_connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    account_id TEXT,
    account_name TEXT,
    access_token_ref TEXT,
    refresh_token_ref TEXT,
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, platform, account_id)
);

-- =============================================================================
-- ETL MANAGEMENT
-- =============================================================================

CREATE TABLE IF NOT EXISTS etl_run_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    run_type TEXT,
    status TEXT,
    records_extracted INTEGER,
    records_loaded INTEGER,
    error_message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- =============================================================================
-- INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_tenant_users_tenant ON tenant_users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_oauth_tenant ON tenant_oauth_connections(tenant_id);
CREATE INDEX IF NOT EXISTS idx_etl_history_tenant ON etl_run_history(tenant_id, platform);
