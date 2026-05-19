"""merge all heads

Revision ID: e3bf4c3b8866
Revises: 1c183a03504e, 2e559856a822
Create Date: 2026-05-12 11:45:22.049377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3bf4c3b8866'
down_revision = ('1c183a03504e', '2e559856a822')
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('org',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('website', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=512), nullable=False),
    sa.Column('address1', sa.String(length=64), nullable=False),
    sa.Column('address2', sa.String(length=64), nullable=False),
    sa.Column('city', sa.String(length=32), nullable=False),
    sa.Column('state', sa.String(length=32), nullable=False),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('org', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_org_name'), ['name'], unique=False)

    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_pair',
    sa.Column('org_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['org_id'], ['org.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('org_id', 'tag_id')
    )


def downgrade():
    pass
