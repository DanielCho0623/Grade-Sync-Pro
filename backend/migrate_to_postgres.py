"""
Script to migrate data from SQLite to PostgreSQL
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from application import create_app, db
from application.models.user import User
from application.models.course import Course
from application.models.assignment import Assignment
from application.models.grade import Grade
from application.models.syllabus_weight import SyllabusWeight
from application.models.notification import Notification

def migrate_data():
    # Create SQLite engine to read from
    sqlite_url = 'sqlite:///instance/gradesync.db'
    sqlite_engine = create_engine(sqlite_url)
    SqliteSession = sessionmaker(bind=sqlite_engine)
    sqlite_session = SqliteSession()
    
    # Create Flask app with PostgreSQL config
    app = create_app('development')
    
    with app.app_context():
        print("Creating PostgreSQL tables...")
        db.create_all()
        print("✓ Tables created")
        
        # Migrate Users
        print("\nMigrating users...")
        users = sqlite_session.query(User).all()
        for user in users:
            # Check if user already exists
            existing = User.query.filter_by(email=user.email).first()
            if not existing:
                db.session.add(user)
        db.session.commit()
        print(f"✓ Migrated {len(users)} users")
        
        # Migrate Courses
        print("\nMigrating courses...")
        courses = sqlite_session.query(Course).all()
        for course in courses:
            # Detach from SQLite session and add to PostgreSQL
            sqlite_session.expunge(course)
            db.session.merge(course)
        db.session.commit()
        print(f"✓ Migrated {len(courses)} courses")
        
        # Migrate Assignments
        print("\nMigrating assignments...")
        assignments = sqlite_session.query(Assignment).all()
        for assignment in assignments:
            sqlite_session.expunge(assignment)
            db.session.merge(assignment)
        db.session.commit()
        print(f"✓ Migrated {len(assignments)} assignments")
        
        # Migrate Grades
        print("\nMigrating grades...")
        grades = sqlite_session.query(Grade).all()
        for grade in grades:
            sqlite_session.expunge(grade)
            db.session.merge(grade)
        db.session.commit()
        print(f"✓ Migrated {len(grades)} grades")
        
        # Migrate Syllabus Weights
        print("\nMigrating syllabus weights...")
        weights = sqlite_session.query(SyllabusWeight).all()
        for weight in weights:
            sqlite_session.expunge(weight)
            db.session.merge(weight)
        db.session.commit()
        print(f"✓ Migrated {len(weights)} syllabus weights")
        
        # Migrate Notifications
        print("\nMigrating notifications...")
        notifications = sqlite_session.query(Notification).all()
        for notification in notifications:
            sqlite_session.expunge(notification)
            db.session.merge(notification)
        db.session.commit()
        print(f"✓ Migrated {len(notifications)} notifications")
        
        print("\n✅ Migration complete!")
        print(f"Total: {len(users)} users, {len(courses)} courses, {len(assignments)} assignments")
    
    sqlite_session.close()

if __name__ == '__main__':
    migrate_data()
