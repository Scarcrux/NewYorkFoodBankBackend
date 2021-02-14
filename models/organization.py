from app import db

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(80))
    contact_name = db.Column(db.String(20))
    phone = db.Column(db.String(10))
    type = db.Column(db.String(20))
    address = db.Column(db.String(80))
    geocode = db.Column(db.String(80))
    hours = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self,organization_name, contact_name, phone, type, address, geocode, hours, user_id):
        self.organization_name = organization_name
        self.contact_name = contact_name
        self.phone = phone
        self.type = type
        self.address = address
        self.geocode = geocode
        self.hours = hours
        self.user_id = user_id

    def json(self):
        return {
            'organization_name': self.organization_name,
            'contact_name': self.contact_name,
            'phone': self.phone,
            'type': self.type,
            'address': self.address,
            'geocode': self.geocode,
            'hours': self.hours
        }
