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

    # Relationships
    assignment = db.relationship('Assignment', back_populates='grade')

    def to_dict(self):
        """Convert grade to dictionary"""
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'points_earned': self.points_earned,
            'percentage': self.percentage,
            'letter_grade': self.letter_grade,
            'graded_date': self.graded_date.isoformat() if self.graded_date else None,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
