from datetime import datetime
from application import db

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
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'brightspace_course_id': self.brightspace_course_id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'semester': self.semester,
            'year': self.year,
            'target_grade': self.target_grade,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_assignments:
            data['assignments'] = [a.to_dict() for a in self.assignments]
        if include_weights:
            data['syllabus_weights'] = [w.to_dict() for w in self.syllabus_weights]
        return data
