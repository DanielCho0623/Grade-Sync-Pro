from datetime import datetime
from app import db

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    brightspace_assignment_id = db.Column(db.String(100))
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))  
    max_points = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship('Course', back_populates='assignments')
    grade = db.relationship('Grade', back_populates='assignment', uselist=False, cascade='all, delete-orphan')

    def to_dict(self, include_grade=False):
