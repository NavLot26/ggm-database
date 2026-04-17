from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Org(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    orgname: so.Mapped[int] = so.mapped_column(sa.String(200), index = True)
    website: so.Mapped[str] = so.mapped_column(sa.String(200))
    description: so.Mapped[str] = so.mapped_column(sa.String(3000))
    address: so.Mapped[str] = so.mapped_column(sa.String(200))

class tagpair(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tag: so.Mapped[str] = so.mapped_column(sa.String(30), primary_key=True)  #this is sketchy i don't think it works