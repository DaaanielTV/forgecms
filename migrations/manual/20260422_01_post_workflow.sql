-- ForgeCMS manual migration
-- Feature set: Post workflow states (draft/scheduled/published/archived)

ALTER TABLE post
    ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'draft' AFTER published,
    ADD COLUMN publish_at DATETIME NULL AFTER status,
    ADD COLUMN published_at DATETIME NULL AFTER publish_at;

-- Backfill existing rows so current behavior is preserved.
UPDATE post
SET
    status = CASE WHEN published = 1 THEN 'published' ELSE 'draft' END,
    published_at = CASE WHEN published = 1 THEN COALESCE(created_at, UTC_TIMESTAMP()) ELSE NULL END
WHERE status IS NULL OR status = '' OR status = 'draft';

-- Helpful index for status-based filtering and scheduling lookups.
CREATE INDEX ix_post_status_publish_at ON post (status, publish_at);
