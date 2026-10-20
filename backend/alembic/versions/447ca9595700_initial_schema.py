"""initial schema

Revision ID: 447ca9595700
Revises: 
Create Date: 2026-10-20 22:09:37.497540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '447ca9595700'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('google_id', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('google_id', name='uq_users_google_id'),
        sa.UniqueConstraint('email', name='uq_users_email'),
    )

    op.create_table(
        'body_measurements',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('height_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('weight_kg', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('bust_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('waist_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('hip_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_body_measurements_user'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_body_measurements_user_id'),
    )

    op.create_table(
        'owned_clothes',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('category', sa.String(length=80), nullable=True),
        sa.Column('brand', sa.String(length=100), nullable=True),
        sa.Column('color', sa.String(length=80), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),
        sa.Column('size_label', sa.String(length=30), nullable=True),
        sa.Column('image_s3_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_owned_clothes_user'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'shops',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('website_url', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'shop_products',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('shop_id', sa.String(length=36), nullable=False),
        sa.Column('external_product_id', sa.String(length=150), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=80), nullable=True),
        sa.Column('color', sa.String(length=80), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),
        sa.Column('image_s3_url', sa.Text(), nullable=True),
        sa.Column('product_url', sa.Text(), nullable=True),
        sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], name='fk_shop_products_shop'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('shop_id', 'external_product_id', name='uq_shop_external_product'),
    )

    op.create_table(
        'size_charts',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('shop_product_id', sa.String(length=36), nullable=False),
        sa.Column('size_label', sa.String(length=30), nullable=False),
        sa.Column('chest_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('waist_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('hip_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('inseam_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('length_cm', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['shop_product_id'], ['shop_products.id'], name='fk_size_charts_product'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'saved_items',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('shop_product_id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_saved_items_user'),
        sa.ForeignKeyConstraint(['shop_product_id'], ['shop_products.id'], name='fk_saved_items_product'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'shop_product_id', name='uq_saved_user_product'),
    )

    op.create_table(
        'outfits',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('preview_image_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_outfits_user'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'outfit_items',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('outfit_id', sa.String(length=36), nullable=False),
        sa.Column('owned_clothes_id', sa.String(length=36), nullable=True),
        sa.Column('shop_product_id', sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(['outfit_id'], ['outfits.id'], name='fk_outfit_items_outfit'),
        sa.ForeignKeyConstraint(['owned_clothes_id'], ['owned_clothes.id'], name='fk_outfit_items_owned_clothes'),
        sa.ForeignKeyConstraint(['shop_product_id'], ['shop_products.id'], name='fk_outfit_items_shop_product'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('outfit_id', 'owned_clothes_id', name='uq_outfit_owned_clothes'),
        sa.UniqueConstraint('outfit_id', 'shop_product_id', name='uq_outfit_shop_product'),
        sa.CheckConstraint(
            "((owned_clothes_id IS NOT NULL AND shop_product_id IS NULL) OR (owned_clothes_id IS NULL AND shop_product_id IS NOT NULL))",
            name='chk_outfit_item_source',
        ),
    )

    op.create_table(
        'try_on_jobs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('outfit_id', sa.String(length=36), nullable=True),
        sa.Column('result_s3_url', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
        sa.Column('provider', sa.String(length=80), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_try_on_jobs_user'),
        sa.ForeignKeyConstraint(['outfit_id'], ['outfits.id'], name='fk_try_on_jobs_outfit'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("status IN ('pending', 'done', 'failed')", name='chk_try_on_job_status'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('try_on_jobs')
    op.drop_table('outfit_items')
    op.drop_table('outfits')
    op.drop_table('saved_items')
    op.drop_table('size_charts')
    op.drop_table('shop_products')
    op.drop_table('shops')
    op.drop_table('owned_clothes')
    op.drop_table('body_measurements')
    op.drop_table('users')
