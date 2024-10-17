"""create montadora table

Revision ID: 1f85d161f1dd
Revises: 
Create Date: 2024-10-16 22:18:57.204693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f85d161f1dd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('montadora',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('pais', sa.String(), nullable=True),
    sa.Column('ano_fundacao', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_montadora_nome'), 'montadora', ['nome'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_montadora_nome'), table_name='montadora')
    op.drop_table('montadora')
    # ### end Alembic commands ###
