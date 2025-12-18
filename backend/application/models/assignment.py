from datetime import datetime
from application import db

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
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'brightspace_assignment_id': self.brightspace_assignment_id,
            'name': self.name,
            'category': self.category,
            'max_points': self.max_points,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_grade and self.grade:
            data['grade'] = self.grade.to_dict()
        return data
