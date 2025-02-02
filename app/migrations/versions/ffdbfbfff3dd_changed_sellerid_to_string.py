from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "ffdbfbfff3dd"
down_revision = "0e6fe26aabc7"
branch_labels = None
depends_on = None


def upgrade():
    # Ensure the `created_at` column has a default value
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'sellers'
              AND column_name = 'created_at'
              AND column_default IS NULL
        ) THEN
            ALTER TABLE sellers ALTER COLUMN created_at SET DEFAULT NOW();
        END IF;
    END $$;
    """)

    # Ensure the `updated_at` column has a default value
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'sellers'
              AND column_name = 'updated_at'
              AND column_default IS NULL
        ) THEN
            ALTER TABLE sellers ALTER COLUMN updated_at SET DEFAULT NOW();
        END IF;
    END $$;
    """)

    # Ensure default values for boolean columns
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'sellers'
              AND column_name = 'is_active'
              AND column_default IS NULL
        ) THEN
            ALTER TABLE sellers ALTER COLUMN is_active SET DEFAULT TRUE;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'sellers'
              AND column_name = 'is_email_verified'
              AND column_default IS NULL
        ) THEN
            ALTER TABLE sellers ALTER COLUMN is_email_verified SET DEFAULT FALSE;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'sellers'
              AND column_name = 'is_phone_verified'
              AND column_default IS NULL
        ) THEN
            ALTER TABLE sellers ALTER COLUMN is_phone_verified SET DEFAULT FALSE;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'sellers'
              AND column_name = 'notifications_enabled'
              AND column_default IS NULL
        ) THEN
            ALTER TABLE sellers ALTER COLUMN notifications_enabled SET DEFAULT TRUE;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'sellers'
              AND column_name = 'ai_recommendation_opt_in'
              AND column_default IS NULL
        ) THEN
            ALTER TABLE sellers ALTER COLUMN ai_recommendation_opt_in SET DEFAULT TRUE;
        END IF;
    END $$;
    """)

    # Backfill default values for existing rows
    op.execute("""
    UPDATE sellers
    SET created_at = NOW()
    WHERE created_at IS NULL;

    UPDATE sellers
    SET updated_at = NOW()
    WHERE updated_at IS NULL;

    UPDATE sellers
    SET is_active = TRUE
    WHERE is_active IS NULL;

    UPDATE sellers
    SET is_email_verified = FALSE
    WHERE is_email_verified IS NULL;

    UPDATE sellers
    SET is_phone_verified = FALSE
    WHERE is_phone_verified IS NULL;

    UPDATE sellers
    SET notifications_enabled = TRUE
    WHERE notifications_enabled IS NULL;

    UPDATE sellers
    SET ai_recommendation_opt_in = TRUE
    WHERE ai_recommendation_opt_in IS NULL;
    """)


def downgrade():
    # Remove default constraints
    op.execute("""
    ALTER TABLE sellers ALTER COLUMN created_at DROP DEFAULT;
    ALTER TABLE sellers ALTER COLUMN updated_at DROP DEFAULT;
    ALTER TABLE sellers ALTER COLUMN is_active DROP DEFAULT;
    ALTER TABLE sellers ALTER COLUMN is_email_verified DROP DEFAULT;
    ALTER TABLE sellers ALTER COLUMN is_phone_verified DROP DEFAULT;
    ALTER TABLE sellers ALTER COLUMN notifications_enabled DROP DEFAULT;
    ALTER TABLE sellers ALTER COLUMN ai_recommendation_opt_in DROP DEFAULT;
    """)
