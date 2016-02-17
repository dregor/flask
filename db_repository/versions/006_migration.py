from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role_association = Table('role_association', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('role_id', INTEGER),
)

Role_association = Table('Role_association', post_meta,
    Column('user_id', Integer),
    Column('role_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=255)),
    Column('last_seen', DateTime),
    Column('about_me', String(length=140)),
    Column('is_active', Boolean),
    Column('is_anonymous', Boolean),
    Column('is_authenticated', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['role_association'].drop()
    post_meta.tables['Role_association'].create()
    post_meta.tables['user'].columns['is_authenticated'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['role_association'].create()
    post_meta.tables['Role_association'].drop()
    post_meta.tables['user'].columns['is_authenticated'].drop()
