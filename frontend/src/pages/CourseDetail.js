import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { coursesAPI, gradesAPI, notificationsAPI } from '../services/api';

function CourseDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [gradeData, setGradeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddWeight, setShowAddWeight] = useState(false);
  const [showAddAssignment, setShowAddAssignment] = useState(false);
  const [showAddGrade, setShowAddGrade] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadCourse();
<<<<<<< HEAD
    // eslint-disable-next-line react-hooks/exhaustive-deps
=======
>>>>>>> 7cd308a (implement course management ui)
  }, [id]);

  const loadCourse = async () => {
    try {
      const [courseRes, gradeRes] = await Promise.all([
        coursesAPI.getCourse(id),
        coursesAPI.calculateGrade(id),
      ]);
      setCourse(courseRes.data);
      setGradeData(gradeRes.data);
    } catch (err) {
      setError('Failed to load course');
    } finally {
      setLoading(false);
    }
  };

  const handleSyncBrightspace = async () => {
    try {
      await coursesAPI.syncCourse(id);
      setSuccess('Synced from Brightspace successfully!');
      loadCourse();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to sync from Brightspace');
    }
  };

  const handleSendAlert = async () => {
    try {
      await notificationsAPI.sendGradeAlert(id, {});
      setSuccess('Grade alert sent successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to send alert');
    }
  };

  const handleDeleteCourse = async () => {
    if (window.confirm('Are you sure you want to delete this course?')) {
      try {
        await coursesAPI.deleteCourse(id);
        navigate('/');
      } catch (err) {
        setError('Failed to delete course');
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading course...</div>;
  }

  if (!course) {
    return <div className="container">Course not found</div>;
  }

  return (
    <div className="container">
      <div style={{ marginBottom: '2rem' }}>
        <button className="btn btn-secondary" onClick={() => navigate('/')}>
          Back to Dashboard
        </button>
      </div>

      {success && <div className="success">{success}</div>}
      {error && <div className="error">{error}</div>}

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
          <div>
            <h2>{course.course_code} - {course.course_name}</h2>
            <p style={{ color: '#666' }}>{course.semester} {course.year}</p>
            <p style={{ marginTop: '1rem' }}>Target Grade: {course.target_grade}%</p>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', flexDirection: 'column' }}>
            <button className="btn" onClick={handleSyncBrightspace}>
              Sync from Brightspace
            </button>
            <button className="btn btn-success" onClick={handleSendAlert}>
              Send Grade Alert
            </button>
            <button className="btn btn-danger" onClick={handleDeleteCourse}>
              Delete Course
            </button>
          </div>
        </div>
      </div>

      {gradeData && !gradeData.error && (
        <div className="card">
          <h3>Current Grade</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
            <div>
              <p style={{ color: '#666', fontSize: '0.9rem' }}>Final Grade</p>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2c3e50' }}>
                {gradeData.final_grade || 'N/A'}%
              </p>
            </div>
            <div>
              <p style={{ color: '#666', fontSize: '0.9rem' }}>Projected Final</p>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3498db' }}>
                {gradeData.projected_final_grade || 'N/A'}%
              </p>
            </div>
            <div>
              <p style={{ color: '#666', fontSize: '0.9rem' }}>Letter Grade</p>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#27ae60' }}>
                {gradeData.letter_grade || 'N/A'}
              </p>
            </div>
            <div>
              <p style={{ color: '#666', fontSize: '0.9rem' }}>Completion</p>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#e67e22' }}>
                {gradeData.completion_percentage || 0}%
              </p>
            </div>
          </div>

          {gradeData.breakdown && gradeData.breakdown.length > 0 && (
            <div style={{ marginTop: '2rem' }}>
              <h4>Grade Breakdown by Category</h4>
              <table>
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>Weight</th>
                    <th>Average</th>
                    <th>Contribution</th>
                  </tr>
                </thead>
                <tbody>
                  {gradeData.breakdown.map((cat, idx) => (
                    <tr key={idx}>
                      <td>{cat.category}</td>
                      <td>{cat.weight}%</td>
                      <td>{cat.average ? `${cat.average.toFixed(2)}%` : 'No grades'}</td>
                      <td>{cat.weighted_contribution ? `${cat.weighted_contribution.toFixed(2)}%` : '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3>Syllabus Weights</h3>
          <button className="btn" onClick={() => setShowAddWeight(true)}>
            Add Weight
          </button>
        </div>
        {course.syllabus_weights && course.syllabus_weights.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Weight</th>
                <th>Description</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {course.syllabus_weights.map((weight) => (
                <tr key={weight.id}>
                  <td>{weight.category}</td>
                  <td>{weight.weight}%</td>
                  <td>{weight.description || '-'}</td>
                  <td>
                    <button
                      className="btn btn-danger"
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.9rem' }}
                      onClick={() => handleDeleteWeight(weight.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No syllabus weights defined. Add weights to calculate your grade.</p>
        )}
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3>Assignments</h3>
          <button className="btn" onClick={() => setShowAddAssignment(true)}>
            Add Assignment
          </button>
        </div>
        {course.assignments && course.assignments.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Category</th>
                <th>Points</th>
                <th>Grade</th>
                <th>Percentage</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {course.assignments.map((assignment) => (
                <tr key={assignment.id}>
                  <td>{assignment.name}</td>
                  <td>{assignment.category}</td>
                  <td>{assignment.max_points}</td>
                  <td>
                    {assignment.grade ? `${assignment.grade.points_earned}/${assignment.max_points}` : '-'}
                  </td>
                  <td>
                    {assignment.grade ? `${assignment.grade.percentage.toFixed(2)}%` : '-'}
                  </td>
                  <td>
                    <button
                      className="btn"
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.9rem', marginRight: '0.5rem' }}
                      onClick={() => {
                        setSelectedAssignment(assignment);
                        setShowAddGrade(true);
                      }}
                    >
                      {assignment.grade ? 'Update' : 'Add'} Grade
                    </button>
                    <button
                      className="btn btn-danger"
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.9rem' }}
                      onClick={() => handleDeleteAssignment(assignment.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No assignments yet. Add assignments to track your grades.</p>
        )}
      </div>

      {showAddWeight && <AddWeightModal courseId={id} onClose={() => { setShowAddWeight(false); loadCourse(); }} />}
      {showAddAssignment && <AddAssignmentModal courseId={id} onClose={() => { setShowAddAssignment(false); loadCourse(); }} />}
      {showAddGrade && <AddGradeModal assignment={selectedAssignment} onClose={() => { setShowAddGrade(false); setSelectedAssignment(null); loadCourse(); }} />}
    </div>
  );

  async function handleDeleteWeight(weightId) {
    if (window.confirm('Are you sure you want to delete this weight?')) {
      try {
        await coursesAPI.deleteWeight(id, weightId);
        setSuccess('Weight deleted successfully!');
        loadCourse();
        setTimeout(() => setSuccess(''), 3000);
      } catch (err) {
        setError('Failed to delete weight');
      }
    }
  }

  async function handleDeleteAssignment(assignmentId) {
    if (window.confirm('Are you sure you want to delete this assignment?')) {
      try {
        await coursesAPI.deleteAssignment(id, assignmentId);
        setSuccess('Assignment deleted successfully!');
        loadCourse();
        setTimeout(() => setSuccess(''), 3000);
      } catch (err) {
        setError('Failed to delete assignment');
      }
    }
  }
}

function AddWeightModal({ courseId, onClose }) {
  const [formData, setFormData] = useState({
    category: '',
    weight: 0,
    description: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await coursesAPI.addWeight(courseId, formData);
      onClose();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add weight');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>Add Syllabus Weight</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Category (e.g., Homework, Exam, Project)</label>
            <input
              type="text"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Weight (%)</label>
            <input
              type="number"
              step="0.1"
              value={formData.weight}
              onChange={(e) => setFormData({ ...formData, weight: parseFloat(e.target.value) })}
              required
            />
          </div>
          <div className="form-group">
            <label>Description (optional)</label>
            <input
              type="text"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>
          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn">
              Add Weight
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function AddAssignmentModal({ courseId, onClose }) {
  const [formData, setFormData] = useState({
    name: '',
    category: 'Homework',
    max_points: 100,
    description: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await coursesAPI.addAssignment(courseId, formData);
      onClose();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add assignment');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>Add Assignment</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Assignment Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Category</label>
            <input
              type="text"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Maximum Points</label>
            <input
              type="number"
              value={formData.max_points}
              onChange={(e) => setFormData({ ...formData, max_points: parseFloat(e.target.value) })}
              required
            />
          </div>
          <div className="form-group">
            <label>Description (optional)</label>
            <input
              type="text"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>
          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn">
              Add Assignment
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function AddGradeModal({ assignment, onClose }) {
  const [formData, setFormData] = useState({
    points_earned: assignment?.grade?.points_earned || 0,
    feedback: assignment?.grade?.feedback || '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await gradesAPI.addGrade(assignment.id, formData);
      onClose();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save grade');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>{assignment?.grade ? 'Update' : 'Add'} Grade for {assignment?.name}</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Points Earned (out of {assignment?.max_points})</label>
            <input
              type="number"
              step="0.1"
              value={formData.points_earned}
              onChange={(e) => setFormData({ ...formData, points_earned: parseFloat(e.target.value) })}
              required
            />
          </div>
          <div className="form-group">
            <label>Feedback (optional)</label>
            <input
              type="text"
              value={formData.feedback}
              onChange={(e) => setFormData({ ...formData, feedback: e.target.value })}
            />
          </div>
          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn">
              Save Grade
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CourseDetail;
