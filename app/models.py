from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

# this is an sql helper table that manages the many to many relationship, it allows the tags to reference all orginizations and the orgs reference all tages 
# still Ms. Wolf's idea of having the tag pair table, but it is just a helper table here and lets SQL know exactly what I am doing 
tag_pair = sa.Table(
    "tag_pair",
    db.metadata,
    sa.Column("org_id", sa.ForeignKey("org.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tag.id"), primary_key=True),
)

class Org(db.Model):
   id: so.Mapped[int] = so.mapped_column(primary_key=True)
   name: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
   website: so.Mapped[str] = so.mapped_column(sa.String(256))
   description: so.Mapped[str] = so.mapped_column(sa.String(512))
   address1: so.Mapped[str] = so.mapped_column(sa.String(64))
   address2: so.Mapped[str] = so.mapped_column(sa.String(64))
   city: so.Mapped[str] = so.mapped_column(sa.String(32))
   state: so.Mapped[str] = so.mapped_column(sa.String(32))
   published: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

   tags: so.Mapped[list["Tag"]] = so.relationship(
        secondary=tag_pair,
        back_populates="orgs"
   )

   def __repr__(self):
       return f'<Org {self.name}>'
   

class Tag(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))

    orgs: so.Mapped[list["Org"]] = so.relationship(
        secondary=tag_pair,
        back_populates="tags"
    )

    def __repr__(self):
       return f'<Tag {self.name}>'

