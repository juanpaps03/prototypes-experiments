"""Initial migration

Revision ID: 0b5cc674430e
Revises: 
Create Date: 2024-12-09 14:01:01.061972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b5cc674430e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('example_data_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_id', sa.UUID(), nullable=False),
    sa.Column('performed_on', sa.DateTime(timezone=True), nullable=False),
    sa.Column('event_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_example_data_event_model_id'), 'example_data_event', ['model_id'], unique=False)
    op.create_table('example_data_created_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['example_data_event.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('example_data_created_event')
    op.drop_index(op.f('ix_example_data_event_model_id'), table_name='example_data_event')
    op.drop_table('example_data_event')
    # ### end Alembic commands ###
