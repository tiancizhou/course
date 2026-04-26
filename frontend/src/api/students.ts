import request from './request'

export function getStudents(params?: { status?: string; keyword?: string }) {
  return request.get('/students', { params })
}

export function getStudent(id: number) {
  return request.get(`/students/${id}`)
}

export function createStudent(data: any) {
  return request.post('/students', data)
}

export function updateStudent(id: number, data: any) {
  return request.put(`/students/${id}`, data)
}

export function deleteStudent(id: number) {
  return request.delete(`/students/${id}`)
}

export function rechargeStudent(id: number, data: { hours: number; remark: string }) {
  return request.post(`/students/${id}/recharge`, data)
}

export function getHourRecords(id: number) {
  return request.get(`/students/${id}/hour-records`)
}
