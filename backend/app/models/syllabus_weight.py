from datetime import datetime
from app import db

class SyllabusWeight(db.Model):
    __tablename__ = 'syllabus_weights'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)  
    weight = db.Column(db.Float, nullable=False)  
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship('Course', back_populates='syllabus_weights')

    __table_args__ = (db.UniqueConstraint('course_id', 'category', name='unique_course_category'),)

    def to_dict(self):
