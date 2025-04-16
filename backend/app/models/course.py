from datetime import datetime
from app import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    brightspace_course_id = db.Column(db.String(100))
    course_code = db.Column(db.String(50), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    semester = db.Column(db.String(50))
    year = db.Column(db.Integer)
    target_grade = db.Column(db.Float, default=85.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='courses')
    assignments = db.relationship('Assignment', back_populates='course', cascade='all, delete-orphan')
    syllabus_weights = db.relationship('SyllabusWeight', back_populates='course', cascade='all, delete-orphan')

    def to_dict(self, include_assignments=False, include_weights=False):
