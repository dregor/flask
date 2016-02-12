from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role = Table('role', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('role_name', String(length=140)),
    Column('user_id', Integer),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('wall_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('role', SMALLINT),
    Column('password', VARCHAR(length=255)),
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
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].create()
    post_meta.tables['post'].columns['wall_id'].create()
    pre_meta.tables['user'].columns['role'].drop()
    post_meta.tables['user'].columns['about_me'].create()
    post_meta.tables['user'].columns['is_active'].create()
    post_meta.tables['user'].columns['is_anonymous'].create()
    post_meta.tables['user'].columns['last_seen'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].drop()
    post_meta.tables['post'].columns['wall_id'].drop()
    pre_meta.tables['user'].columns['role'].create()
    post_meta.tables['user'].columns['about_me'].drop()
    post_meta.tables['user'].columns['is_active'].drop()
    post_meta.tables['user'].columns['is_anonymous'].drop()
    post_meta.tables['user'].columns['last_seen'].drop()
