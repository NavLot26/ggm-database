from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

# Table that connects orgasnizations to tags
org_tags = sa.Table(
    'org_tags',
    db.metadata,

    # The organization id and tag id together form the primary key
    sa.Column('org_id', sa.Integer, sa.ForeignKey('org.id'), primary_key=True),
    sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id'), primary_key=True)
)

# Admin user login
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Org(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    orgname: so.Mapped[SystemError] = so.mapped_column(sa.String(64), index = True)
    website: so.Mapped[str] = so.mapped_column(sa.String(200))
    description: so.Mapped[str] = so.mapped_column(sa.String(1000))
    address1: so.Mapped[str] = so.mapped_column(sa.String(128))
    address2: so.Mapped[str] = so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), nullable=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64))
    state: so.Mapped[str] = so.mapped_column(sa.String(64))
    published: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    tags: so.Mapped[list] = so.relationship('Tag', secondary=org_tags, back_populates='orgs')

    def __repr__(self):
        return f'<Org {self.orgname}>'
    


@login.user_loader
def load_user(id):
    return User.query.get(int(id))