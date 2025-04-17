import axios from 'axios';

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';
=======
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
>>>>>>> d45cd62 (add api services and auth)
=======
const API_URL = process.env.REACT_APP_API_URL || 'http:
>>>>>>> 4990274 (clean up code)
=======
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
>>>>>>> 5aa3e2d (restore function implementations)

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
  updateUser: (data) => api.put('/auth/me', data),
};

export const coursesAPI = {
  getCourses: () => api.get('/courses/'),
  getCourse: (id) => api.get(`/courses/${id}`),
  createCourse: (data) => api.post('/courses/', data),
  updateCourse: (id, data) => api.put(`/courses/${id}`, data),
  deleteCourse: (id) => api.delete(`/courses/${id}`),
  syncCourse: (id) => api.post(`/courses/${id}/sync`),
  calculateGrade: (id) => api.get(`/courses/${id}/calculate`),
  calculateGradeNeeded: (id, target) => api.get(`/courses/${id}/grade-needed?target=${target}`),
  addWeight: (id, data) => api.post(`/courses/${id}/weights`, data),
  deleteWeight: (courseId, weightId) => api.delete(`/courses/${courseId}/weights/${weightId}`),
  addAssignment: (id, data) => api.post(`/courses/${id}/assignments`, data),
  deleteAssignment: (courseId, assignmentId) => api.delete(`/courses/${courseId}/assignments/${assignmentId}`),
};

export const gradesAPI = {
  addGrade: (assignmentId, data) => api.post(`/grades/assignment/${assignmentId}`, data),
  getGrade: (assignmentId) => api.get(`/grades/assignment/${assignmentId}`),
  deleteGrade: (assignmentId) => api.delete(`/grades/assignment/${assignmentId}`),
  getCourseGrades: (courseId) => api.get(`/grades/course/${courseId}`),
};

export const notificationsAPI = {
  getNotifications: () => api.get('/notifications/'),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
  sendGradeAlert: (courseId, data) => api.post(`/notifications/send-grade-alert/${courseId}`, data),
  autoCheckGrades: () => api.post('/notifications/auto-check'),
};

export default api;
