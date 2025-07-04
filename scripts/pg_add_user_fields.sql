-- Migration to add missing columns for per-user integrations and MFA
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS slack_webhook_url VARCHAR(255),
  ADD COLUMN IF NOT EXISTS webhook_url VARCHAR(255),
  ADD COLUMN IF NOT EXISTS mfa_enabled BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS mfa_secret VARCHAR(255);
