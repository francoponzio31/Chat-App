"""chat_participants table renamed

Revision ID: ba0f6894718f
Revises: f8a3a9673504
Create Date: 2024-03-26 23:09:44.172282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba0f6894718f'
down_revision: Union[str, None] = 'f8a3a9673504'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts')
    op.drop_table('chat_participant')
    op.drop_table('users')
    op.drop_table('chats')
    op.drop_table('messages')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('chat_id', sa.INTEGER(), nullable=False),
    sa.Column('sender_user_id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.VARCHAR(), nullable=False),
    sa.Column('sent_date', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.ForeignKeyConstraint(['sender_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chats',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('is_group', sa.BOOLEAN(), nullable=False),
    sa.Column('group_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('creation_date', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=320), nullable=False),
    sa.Column('username', sa.VARCHAR(length=40), nullable=False),
    sa.Column('password', sa.VARCHAR(length=45), nullable=True),
    sa.Column('role', sa.VARCHAR(length=5), nullable=False),
    sa.Column('picture_id', sa.VARCHAR(length=36), nullable=True),
    sa.Column('creation_date', sa.DATETIME(), nullable=False),
    sa.Column('last_connection', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('chat_participant',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('chat_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('joined_date', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('contact_user_id', sa.INTEGER(), nullable=False),
    sa.Column('added_date', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['contact_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###