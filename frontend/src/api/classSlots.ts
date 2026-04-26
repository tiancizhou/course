import request from './request'

export function getClassSlots(params?: { is_active?: boolean }) {
  return request.get('/class-slots', { params })
}

export function getClassSlot(id: number) {
  return request.get(`/class-slots/${id}`)
}

export function createClassSlot(data: any) {
  return request.post('/class-slots', data)
}

export function updateClassSlot(id: number, data: any) {
  return request.put(`/class-slots/${id}`, data)
}

export function deleteClassSlot(id: number) {
  return request.delete(`/class-slots/${id}`)
}

export function addSlotStudent(slotId: number, data: { student_id: number; start_date: string }) {
  return request.post(`/class-slots/${slotId}/students`, data)
}

export function removeSlotStudent(slotId: number, studentId: number) {
  return request.delete(`/class-slots/${slotId}/students/${studentId}`)
}
