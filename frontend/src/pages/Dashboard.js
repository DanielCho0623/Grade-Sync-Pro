import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { coursesAPI, notificationsAPI } from '../services/api';

function Dashboard() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddCourse, setShowAddCourse] = useState(false);
  const [formData, setFormData] = useState({
    course_code: '',
    course_name: '',
    semester: '',
    year: new Date().getFullYear(),
    target_grade: 85,
  });
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const response = await coursesAPI.getCourses();
<<<<<<< HEAD
<<<<<<< HEAD
      setCourses(response.data.courses);
=======
      setCourses(response.data);
>>>>>>> 191e1da (create course dashboard)
=======
      setCourses(response.data.courses);
>>>>>>> 7bd7713 (fix dashboard courses data)
    } catch (err) {
      setError('Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  const handleAddCourse = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await coursesAPI.createCourse(formData);
      setSuccess('Course added successfully!');
      setShowAddCourse(false);
      setFormData({
        course_code: '',
        course_name: '',
        semester: '',
        year: new Date().getFullYear(),
        target_grade: 85,
      });
      loadCourses();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add course');
    }
  };

  const handleAutoCheck = async () => {
    try {
      const response = await notificationsAPI.autoCheckGrades();
      setSuccess(response.data.message);
      setTimeout(() => setSuccess(''), 5000);
    } catch (err) {
      setError('Failed to check grades');
    }
  };

  const getGradeClass = (letterGrade) => {
    if (!letterGrade) return '';
    const grade = letterGrade[0];
    return `grade-${grade}`;
  };

  if (loading) {
    return <div className="loading">Loading courses...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>My Courses</h2>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-secondary" onClick={handleAutoCheck}>
            Check All Grades
          </button>
          <button className="btn" onClick={() => setShowAddCourse(true)}>
            Add Course
          </button>
        </div>
      </div>

      {success && <div className="success">{success}</div>}
      {error && <div className="error">{error}</div>}

      {courses.length === 0 ? (
        <div className="card">
          <p>No courses yet. Add your first course to get started!</p>
        </div>
      ) : (
        <div className="course-list">
          {courses.map((course) => (
            <CourseCard key={course.id} course={course} navigate={navigate} getGradeClass={getGradeClass} />
          ))}
        </div>
      )}

      {showAddCourse && (
        <div className="modal-overlay" onClick={() => setShowAddCourse(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Course</h2>
            <form onSubmit={handleAddCourse}>
              <div className="form-group">
                <label>Course Code</label>
                <input
                  type="text"
                  value={formData.course_code}
                  onChange={(e) => setFormData({ ...formData, course_code: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Course Name</label>
                <input
                  type="text"
                  value={formData.course_name}
                  onChange={(e) => setFormData({ ...formData, course_name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Semester</label>
                <input
                  type="text"
                  value={formData.semester}
                  onChange={(e) => setFormData({ ...formData, semester: e.target.value })}
                  placeholder="e.g., Spring, Fall"
                />
              </div>
              <div className="form-group">
                <label>Year</label>
                <input
                  type="number"
                  value={formData.year}
                  onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
                />
              </div>
              <div className="form-group">
                <label>Target Grade (%)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.target_grade}
                  onChange={(e) => setFormData({ ...formData, target_grade: parseFloat(e.target.value) })}
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAddCourse(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn">
                  Add Course
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function CourseCard({ course, navigate, getGradeClass }) {
  const [gradeData, setGradeData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGradeData();
<<<<<<< HEAD
<<<<<<< HEAD
    // eslint-disable-next-line react-hooks/exhaustive-deps
=======
>>>>>>> 191e1da (create course dashboard)
=======
    // eslint-disable-next-line react-hooks/exhaustive-deps
>>>>>>> 661277e (fix eslint warnings in production build)
  }, []);

  const loadGradeData = async () => {
    try {
      const response = await coursesAPI.calculateGrade(course.id);
      setGradeData(response.data);
    } catch (err) {
      console.error('Failed to load grade data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="course-item" onClick={() => navigate(`/course/${course.id}`)}>
      <div className="course-header">
        <div>
          <h3>{course.course_code}</h3>
          <p style={{ color: '#666', margin: '0.5rem 0' }}>{course.course_name}</p>
          <p style={{ color: '#999', fontSize: '0.9rem' }}>
            {course.semester} {course.year}
          </p>
        </div>
        {!loading && gradeData && gradeData.projected_final_grade && (
          <div className={`grade-badge ${getGradeClass(gradeData.letter_grade)}`}>
            {gradeData.projected_final_grade}%
            <div style={{ fontSize: '0.9rem' }}>{gradeData.letter_grade}</div>
          </div>
        )}
      </div>
      {!loading && gradeData && (
        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #eee' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
            <span>Target: {course.target_grade}%</span>
            <span>Completion: {gradeData.completion_percentage}%</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
