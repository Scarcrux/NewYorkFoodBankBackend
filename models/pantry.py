from app import db

class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pantry_name = db.Column(db.String(80))
    contact_name = db.Column(db.String(20))
    phone = db.Column(db.String(10))
    type = db.Column(db.String(20))
    address = db.Column(db.String(80))
    geocode = db.Column(db.String(80))
    hours = db.Column(db.String(200))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    def __init__(self, pantry_name, contact_name, phone, type, address, geocode, hours, organization_id):
        self.pantry_name = pantry_name
        self.contact_name = contact_name
        self.phone = phone
        self.type = type
        self.address = address
        self.geocode = geocode
        self.hours = hours
        self.organization_id = organization_id

    def json(self):
        return {
            'pantry_name': self.pantry_name,
            'contact_name': self.contact_name,
            'phone': self.phone,
            'type': self.type,
            'address': self.address,
            'geocode': self.geocode,
            'hours': self.hours
        }