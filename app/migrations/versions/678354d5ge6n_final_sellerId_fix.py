from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "678354d5ge6n"
down_revision = "ffdbfbfff3dd"
branch_labels = None
depends_on = None


def upgrade():
    # Create the set_default_sellerId function
    op.execute("""
    CREATE OR REPLACE FUNCTION public.set_default_sellerId()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW."sellerId" IS NULL THEN
            NEW."sellerId" := NEW.id::VARCHAR; -- Cast `id` to string
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Create the trigger on the sellers table
    op.execute("""
    CREATE TRIGGER trigger_set_sellerId
    BEFORE INSERT ON public.sellers
    FOR EACH ROW
    EXECUTE FUNCTION public.set_default_sellerId();
    """)



def downgrade():
    # Step 1: Drop the trigger if it exists
    op.execute("""
    DROP TRIGGER IF EXISTS trigger_set_sellerId ON sellers;
    """)

    # Step 2: Drop the function if it exists
    op.execute("""
    DROP FUNCTION IF EXISTS set_default_sellerId();
    """)
