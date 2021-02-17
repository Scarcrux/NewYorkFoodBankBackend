from app import db
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(80))
    contact_name = db.Column(db.String(20))
    phone = db.Column(db.String(14))
    type = db.Column(db.String(20))
    address = db.Column(db.String(80))
    url = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, organization_name, type, address, phone, url, user_id):
        self.organization_name = organization_name
        self.phone = phone
        self.type = type
        self.address = address
        self.url = url
        self.user_id = user_id

    def json(self):
        return {
            'organization_name': self.organization_name,
            'phone': self.phone,
            'type': self.type,
            'address': self.address,
            'url': self.url
        }
