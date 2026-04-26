<template>
  <div class="home">
    <!-- Header -->
    <div class="home-header">
      <div class="header-date">{{ todayLabel }}</div>
      <div class="header-sub">{{ todayDate }}</div>
      <div class="header-mascot">( ᵔ ᴥ ᵔ )</div>
    </div>

    <!-- Warnings -->
    <div class="warning-card k-card" v-if="dashboard.low_hour_students.length" @click="showLowHours=!showLowHours" style="background: var(--bg-cream);">
      <div class="warning-text">⚡ {{ dashboard.low_hour_students.length }} 位学生课时不足</div>
      <div class="warning-detail" v-if="showLowHours">
        <div v-for="s in dashboard.low_hour_students" :key="s.id" class="warning-item" @click.stop="$router.push(`/students/${s.id}`)">
          <span>{{ s.name }}</span>
          <span class="badge badge-warn">{{ s.remaining_hours }} 课时</span>
        </div>
      </div>
    </div>
    <div class="warning-card k-card" v-if="dashboard.zero_hour_students.length" @click="showZeroHours=!showZeroHours" style="background: var(--bg-pink);">
      <div class="warning-text">♡ {{ dashboard.zero_hour_students.length }} 位学生欠课时</div>
      <div class="warning-detail" v-if="showZeroHours">
        <div v-for="s in dashboard.zero_hour_students" :key="s.id" class="warning-item" @click.stop="$router.push(`/students/${s.id}`)">
          <span>{{ s.name }}</span>
          <span class="badge badge-danger">{{ s.remaining_hours }} 课时</span>
        </div>
      </div>
    </div>

    <!-- Today's classes -->
    <div class="k-section">今日课程</div>

    <div v-if="dashboard.today_lessons.length === 0" class="empty-card k-card">
      <div class="empty-icon">🌿</div>
      <div class="empty-text">今天没有课，好好休息吧</div>
    </div>

    <div v-for="lesson in dashboard.today_lessons" :key="lesson.id" class="lesson-card k-card" :class="{ done: lesson.status === 'completed' }">
      <div class="lc-top">
        <div class="lc-name">{{ lesson.slot_name || '临时课' }}</div>
        <span class="lc-status" :class="lesson.status">{{ statusMap[lesson.status] }}</span>
      </div>
      <div class="lc-info">
        <span>{{ lesson.start_time?.slice(0,5) }} - {{ lesson.end_time?.slice(0,5) }}</span>
        <span>{{ lesson.student_count }} 位学生</span>
      </div>
      <button class="k-btn k-btn-pink lc-btn" @click="$router.push(`/lessons/${lesson.id}/attendance`)" style="width:100%">
        {{ lesson.status === 'completed' ? '查看记录' : '开始点名' }}
      </button>
    </div>

    <!-- Week preview -->
    <div class="k-section">本周课程</div>
    <div v-if="dashboard.week_lessons.length === 0" class="empty-card k-card">
      <div class="empty-text">本周暂无课程</div>
    </div>
    <div v-else class="week-card k-card">
      <div v-for="lesson in dashboard.week_lessons" :key="lesson.id" class="wk-item" @click="$router.push(`/lessons/${lesson.id}/attendance`)">
        <div class="wk-day">{{ weekdayShort[lesson.weekday] }}</div>
        <div class="wk-info">
          <div class="wk-name">{{ lesson.slot_name || '临时课' }}</div>
          <div class="wk-time">{{ lesson.start_time?.slice(0,5) }}-{{ lesson.end_time?.slice(0,5) }}</div>
        </div>
        <span class="lc-status" :class="lesson.status">{{ statusMap[lesson.status] }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getDashboard } from '@/api/dashboard'

const weekdayNames = ['周一','周二','周三','周四','周五','周六','周日']
const weekdayShort = ['一','二','三','四','五','六','日']
const statusMap: Record<string,string> = { scheduled:'待上课', completed:'已完成', cancelled:'已取消' }

const dashboard = ref<any>({ total_students:0, today_lessons:[], week_lessons:[], low_hour_students:[], zero_hour_students:[], today_pending_count:0 })
const showLowHours = ref(false)
const showZeroHours = ref(false)

const todayDate = computed(() => { const d=new Date(); return `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日` })
const todayLabel = computed(() => { const d=new Date(); return `今天 · ${weekdayNames[(d.getDay()+6)%7]}` })

async function loadData() { const res:any = await getDashboard(); dashboard.value = res.data }
onMounted(loadData)
</script>

<style scoped>
.home { padding-bottom: 20px; }

.home-header {
  text-align: center;
  padding: 12px 0 20px;
}
.header-date { font-size: 22px; font-weight: 700; color: var(--text-primary); }
.header-sub { font-size: 13px; color: var(--text-secondary); margin-top: 2px; }
.header-mascot { font-size: 28px; margin-top: 6px; }

/* Warning */
.warning-card { margin-bottom: 10px; cursor: pointer; }
.warning-text { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.warning-detail { margin-top: 8px; }
.warning-item { display:flex; justify-content:space-between; align-items:center; padding:5px 0; font-size:13px; }

.badge { font-size:11px; padding:2px 8px; border-radius:10px; font-weight:600; }
.badge-warn { background:var(--cream-soft); color:#B8941E; }
.badge-danger { background:var(--pink-soft); color:#D4647A; }

/* Lesson card */
.lesson-card { margin-bottom: 12px; }
.lesson-card.done { opacity: 0.65; }
.lc-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
.lc-name { font-size:16px; font-weight:700; }
.lc-status { font-size:11px; padding:3px 8px; border-radius:8px; font-weight:500; }
.lc-status.scheduled { background:var(--cream-soft); color:#B8941E; }
.lc-status.completed { background:var(--mint-soft); color:#4AA898; }
.lc-status.cancelled { background:#f2f2f5; color:#aaa; }
.lc-info { display:flex; gap:14px; font-size:13px; color:var(--text-secondary); margin-bottom:12px; }
.lc-btn { font-size:15px; padding:12px; }

/* Empty */
.empty-card { text-align:center; padding:28px 16px; }
.empty-icon { font-size:32px; margin-bottom:8px; }
.empty-text { color:var(--text-hint); font-size:14px; }

/* Week */
.week-card { padding:4px 0; }
.wk-item { display:flex; align-items:center; padding:10px 16px; border-bottom:1px solid #F5F2F8; cursor:pointer; }
.wk-item:last-child { border-bottom:none; }
.wk-item:active { background:#FAF7FD; }
.wk-day { width:28px; font-size:12px; color:var(--text-hint); font-weight:600; flex-shrink:0; }
.wk-info { flex:1; margin-left:8px; }
.wk-name { font-size:14px; font-weight:500; }
.wk-time { font-size:11px; color:var(--text-hint); margin-top:1px; }
</style>
