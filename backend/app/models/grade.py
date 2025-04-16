from datetime import datetime
from app import db

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False, unique=True)
    points_earned = db.Column(db.Float)
    percentage = db.Column(db.Float)
    letter_grade = db.Column(db.String(5))
    graded_date = db.Column(db.DateTime)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignment = db.relationship('Assignment', back_populates='grade')

    def to_dict(self):
