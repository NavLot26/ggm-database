from app import app, db
from app.models import Tag 

app.app_context().push()


start_tags = [
    "Direct Service",
    "Environmental",
    "Food Insecurity",
    "Housing Insecurity",
    "Animals",
    "Children",
    "Elderly",
    "Over 16",
    "Health/Medical",
]

# just init and add each tag to the db
for tag_name in start_tags: 
    tag = Tag(name = tag_name)
    db.session.add(tag)

db.session.commit()
