from database import db

class Student(db.Model):
    __tablename__ = 'students'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    course = db.Column(db.String, nullable=True) 
    photo_url = db.Column(db.String, nullable=True)