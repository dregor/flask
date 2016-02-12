from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role_association = Table('role_association', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('role_id', Integer, primary_key=True, nullable=False),
)

role = Table('role', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('role_name', VARCHAR(length=140)),
    Column('user_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role_association'].create()
    pre_meta.tables['role'].columns['user_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role_association'].drop()
    pre_meta.tables['role'].columns['user_id'].create()
