"""created users table

Revision ID: 18d09af8a984
Revises: 
Create Date: 2023-11-10 15:06:20.009123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '18d09af8a984'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('profile_picture', sa.String(length=255), server_default=sa.text("'https://res.cloudinary.com/dxgl4eyhq/image/upload/v1699608195/sms/profile/default_profile.jpg'"), nullable=True),
    sa.Column('is_active', mysql.TINYINT(), server_default=sa.text('1'), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'OTHERS', name='genderenum'), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
