import csv 
from app import app, db 
from app.models import Org  

app.app_context().push()


with open('sheet.csv', newline='') as sheet: 
    reader = csv.DictReader(sheet)
    
    for row in reader: 
        org = Org(
            name=row["name"], 
            website=row.get("website", ""),
            description=row.get("description", ""),
            address1=row.get("address1", ""),
            address2=row.get("address2", ""),
            city=row.get("city", ""),
            state=row.get("state", ""),
            published=True
        )

        db.session.add(org)
    db.session.commit()