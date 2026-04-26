import request from './request'

export function getTerms() {
  return request.get('/terms')
}

export function getTerm(id: number) {
  return request.get(`/terms/${id}`)
}

export function createTerm(data: any) {
  return request.post('/terms', data)
}

export function updateTerm(id: number, data: any) {
  return request.put(`/terms/${id}`, data)
}

export function deleteTerm(id: number) {
  return request.delete(`/terms/${id}`)
}

export function generateLessons(termId: number) {
  return request.post(`/terms/${termId}/generate-lessons`)
}
