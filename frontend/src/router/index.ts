import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
  { path: '/students', name: 'Students', component: () => import('@/views/Students.vue') },
  { path: '/students/:id', name: 'StudentDetail', component: () => import('@/views/StudentDetail.vue') },
  { path: '/class-slots', name: 'ClassSlots', component: () => import('@/views/ClassSlots.vue') },
  { path: '/terms', name: 'Terms', component: () => import('@/views/Terms.vue') },
  { path: '/lessons', name: 'Lessons', component: () => import('@/views/Lessons.vue') },
  { path: '/lessons/:id/attendance', name: 'LessonAttendance', component: () => import('@/views/LessonAttendance.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
