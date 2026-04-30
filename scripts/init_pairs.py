import csv
from app import app, db
from app.models import Org, Tag


# init the app context allowing us to access the database
app.app_context().push()

with open('pairs.csv', newline='') as pairs: 
    reader = csv.DictReader(pairs)

    # for each row we get the org and tag id, then get the org and tags
    for row in reader:
        org_id = int(row["org index"])
        tag_id = int(row["tag index"])

        org = db.session.get(Org, org_id)
        tag = db.session.get(Tag, tag_id)

        org.tags.append(tag) # this adds the tag to the org relationship and vice versa using the automated helper table

    db.session.commit()

    