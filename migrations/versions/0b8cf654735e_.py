"""empty message

Revision ID: 0b8cf654735e
Revises: a2c073252b1d
Create Date: 2017-12-10 15:45:25.653001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b8cf654735e'
down_revision = 'a2c073252b1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('choices', sa.Column('pos_id', sa.Integer(), nullable=False))
    op.drop_constraint('choices_part_of_speech_id_fkey', 'choices', type_='foreignkey')
    op.create_foreign_key(None, 'choices', 'part_of_speeches', ['pos_id'], ['id'])
    op.drop_column('choices', 'part_of_speech_id')
    op.add_column('users', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('users', sa.Column('modified_date', sa.DateTime(), nullable=False))
    op.add_column('words', sa.Column('choice_1_id', sa.Integer(), nullable=False))
    op.add_column('words', sa.Column('choice_2_id', sa.Integer(), nullable=False))
    op.add_column('words', sa.Column('choice_3_id', sa.Integer(), nullable=False))
    op.add_column('words', sa.Column('pos_id', sa.Integer(), nullable=False))
    op.add_column('words', sa.Column('weight', sa.Integer(), nullable=False))
    op.drop_constraint('words_choice_3_fkey', 'words', type_='foreignkey')
    op.drop_constraint('words_part_of_speech_id_fkey', 'words', type_='foreignkey')
    op.drop_constraint('words_choice_1_fkey', 'words', type_='foreignkey')
    op.drop_constraint('words_choice_2_fkey', 'words', type_='foreignkey')
    op.create_foreign_key(None, 'words', 'choices', ['choice_1_id'], ['id'])
    op.create_foreign_key(None, 'words', 'part_of_speeches', ['pos_id'], ['id'])
    op.create_foreign_key(None, 'words', 'choices', ['choice_2_id'], ['id'])
    op.create_foreign_key(None, 'words', 'choices', ['choice_3_id'], ['id'])
    op.drop_column('words', 'choice_3')
    op.drop_column('words', 'choice_1')
    op.drop_column('words', 'choice_2')
    op.drop_column('words', 'wight')
    op.drop_column('words', 'part_of_speech_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('part_of_speech_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('words', sa.Column('wight', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('words', sa.Column('choice_2', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('words', sa.Column('choice_1', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('words', sa.Column('choice_3', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'words', type_='foreignkey')
    op.drop_constraint(None, 'words', type_='foreignkey')
    op.drop_constraint(None, 'words', type_='foreignkey')
    op.drop_constraint(None, 'words', type_='foreignkey')
    op.create_foreign_key('words_choice_2_fkey', 'words', 'choices', ['choice_2'], ['id'])
    op.create_foreign_key('words_choice_1_fkey', 'words', 'choices', ['choice_1'], ['id'])
    op.create_foreign_key('words_part_of_speech_id_fkey', 'words', 'part_of_speeches', ['part_of_speech_id'], ['id'])
    op.create_foreign_key('words_choice_3_fkey', 'words', 'choices', ['choice_3'], ['id'])
    op.drop_column('words', 'weight')
    op.drop_column('words', 'pos_id')
    op.drop_column('words', 'choice_3_id')
    op.drop_column('words', 'choice_2_id')
    op.drop_column('words', 'choice_1_id')
    op.drop_column('users', 'modified_date')
    op.drop_column('users', 'created_date')
    op.add_column('choices', sa.Column('part_of_speech_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'choices', type_='foreignkey')
    op.create_foreign_key('choices_part_of_speech_id_fkey', 'choices', 'part_of_speeches', ['part_of_speech_id'], ['id'])
    op.drop_column('choices', 'pos_id')
    # ### end Alembic commands ###