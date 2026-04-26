import request from './request'

export function getLessons(params?: any) {
  return request.get('/lessons', { params })
}

export function getLesson(id: number) {
  return request.get(`/lessons/${id}`)
}

export function createLesson(data: any) {
  return request.post('/lessons', data)
}

export function updateLesson(id: number, data: any) {
  return request.put(`/lessons/${id}`, data)
}

export function deleteLesson(id: number) {
  return request.delete(`/lessons/${id}`)
}

export function getLessonStudents(lessonId: number) {
  return request.get(`/lessons/${lessonId}/students`)
}

export function addLessonStudent(lessonId: number, data: { student_id: number; source_type?: string }) {
  return request.post(`/lessons/${lessonId}/students`, data)
}

export function removeLessonStudent(lessonId: number, studentId: number) {
  return request.delete(`/lessons/${lessonId}/students/${studentId}`)
}

export function takeAttendance(lessonId: number, records: any[]) {
  return request.post(`/lessons/${lessonId}/attendance`, records)
}
