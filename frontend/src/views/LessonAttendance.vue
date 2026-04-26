<template>
  <div class="att-page">
    <!-- Top bar -->
    <div class="k-top">
      <button class="k-top-back" @click="$router.back()">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>
        返回
      </button>
      <span class="k-top-title">课程点名</span>
    </div>

    <!-- Lesson info card -->
    <div class="lesson-info k-card" v-if="lesson">
      <div class="li-name">{{ lesson.slot_name || '临时课' }}</div>
      <div class="li-sub">{{ lesson.lesson_date }} {{ weekdayNames[lesson.weekday] }} · {{ lesson.start_time?.slice(0,5) }}-{{ lesson.end_time?.slice(0,5) }}</div>
    </div>

    <!-- Student list -->
    <div class="stu-list">
      <div v-for="s in lessonStudents" :key="s.student_id" class="stu-card k-card">
        <div class="stu-name">{{ s.student_name }}</div>
        <div class="stu-btns">
          <button class="stu-btn present" :class="{ active: s.attendance_status === 'present' }" @click="setStatus(s,'present')">到课</button>
          <button class="stu-btn leave" :class="{ active: s.attendance_status === 'leave' }" @click="setStatus(s,'leave')">请假</button>
          <button class="stu-btn absent" :class="{ active: s.attendance_status === 'absent' }" @click="setStatus(s,'absent')">缺席</button>
        </div>
        <div class="deduct-row" v-if="s.attendance_status === 'absent'">
          <span class="deduct-label">扣课时</span>
          <label class="switch-wrap">
            <input type="checkbox" v-model="s.deduct_flag" @change="s.deduct_hours = s.deduct_flag ? 1 : 0">
            <span class="switch-track"></span>
          </label>
        </div>
      </div>
    </div>

    <!-- Add student -->
    <div class="add-row" @click="showAddDialog = true">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="var(--pink)" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
      <span>添加学生</span>
    </div>

    <!-- Fixed submit -->
    <div class="submit-bar">
      <button class="k-btn k-btn-pink" style="width:100%; padding:14px; font-size:16px;" @click="handleSubmit">
        提交点名 ({{ lessonStudents.length }} 人)
      </button>
    </div>

    <!-- Add dialog -->
    <el-dialog v-model="showAddDialog" title="添加学生" width="340px" :append-to-body="true">
      <el-form label-position="top">
        <el-form-item label="选择学生">
          <el-select v-model="addForm.student_id" filterable placeholder="搜索学生" style="width:100%">
            <el-option v-for="s in allStudents" :key="s.id" :label="`${s.name}（剩余 ${s.remaining_hours}）`" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="来源">
          <el-select v-model="addForm.source_type" style="width:100%">
            <el-option label="手动添加" value="manual" />
            <el-option label="补课" value="makeup" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog=false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getLesson, getLessonStudents, addLessonStudent, takeAttendance } from '@/api/lessons'
import { getStudents } from '@/api/students'

const route = useRoute()
const lessonId = Number(route.params.id)
const lesson = ref<any>(null)
const lessonStudents = ref<any[]>([])
const allStudents = ref<any[]>([])
const showAddDialog = ref(false)
const addForm = ref<any>({ student_id: undefined, source_type: 'manual' })

const weekdayNames = ['周一','周二','周三','周四','周五','周六','周日']

async function loadData() {
  const [lRes, sRes, aRes]: any[] = await Promise.all([
    getLesson(lessonId), getLessonStudents(lessonId), getStudents({ status: 'active' })
  ])
  lesson.value = lRes.data
  allStudents.value = aRes.data
  lessonStudents.value = sRes.data.map((s: any) => ({
    ...s,
    attendance_status: s.attendance_status === 'pending' ? 'present' : s.attendance_status,
    deduct_hours: Number(s.hour_change) < 0 ? Math.abs(Number(s.hour_change)) : (s.attendance_status === 'leave' ? 0 : 1),
    deduct_flag: Number(s.hour_change) < 0 ? true : (s.attendance_status !== 'leave'),
  }))
}

function setStatus(s: any, status: string) {
  s.attendance_status = status
  s.deduct_hours = status === 'leave' ? 0 : 1
  s.deduct_flag = status !== 'leave'
}

async function handleAdd() {
  await addLessonStudent(lessonId, addForm.value)
  ElMessage.success('添加成功'); showAddDialog.value = false; loadData()
}

async function handleSubmit() {
  const records = lessonStudents.value.map(s => ({
    student_id: s.student_id, attendance_status: s.attendance_status, deduct_hours: Number(s.deduct_hours || 0)
  }))
  await takeAttendance(lessonId, records)
  ElMessage.success('点名成功 ✓'); loadData()
}

onMounted(loadData)
</script>

<style scoped>
.att-page { padding-bottom: 90px; }

.lesson-info { text-align:center; margin-bottom:14px; }
.li-name { font-size:18px; font-weight:700; }
.li-sub { font-size:13px; color:var(--text-secondary); margin-top:4px; }

/* Student card */
.stu-list { display:flex; flex-direction:column; gap:10px; }
.stu-card { padding:14px; }
.stu-name { font-size:15px; font-weight:600; margin-bottom:10px; }

.stu-btns { display:flex; gap:8px; }
.stu-btn {
  flex:1; height:40px; border:2px solid #EDE8F5; border-radius:var(--radius-m);
  background:#fff; font-size:14px; font-weight:600; color:var(--text-secondary);
  cursor:pointer; transition: all 0.2s ease; font-family:inherit;
}
.stu-btn:active { transform:scale(0.95); }
.stu-btn.present.active { background:var(--mint-soft); border-color:var(--mint); color:#3D9E8E; }
.stu-btn.leave.active { background:var(--cream-soft); border-color:var(--cream); color:#B8941E; }
.stu-btn.absent.active { background:var(--pink-soft); border-color:var(--pink); color:#D4647A; }

.deduct-row { display:flex; align-items:center; justify-content:flex-end; gap:8px; margin-top:8px; }
.deduct-label { font-size:12px; color:var(--text-hint); }

/* Custom switch */
.switch-wrap { position:relative; width:44px; height:24px; }
.switch-wrap input { display:none; }
.switch-track {
  position:absolute; top:0; left:0; right:0; bottom:0;
  background:#E0DCE8; border-radius:12px; transition:0.25s; cursor:pointer;
}
.switch-track::after {
  content:''; position:absolute; width:20px; height:20px; border-radius:50%;
  background:#fff; top:2px; left:2px; transition:0.25s; box-shadow:0 1px 4px rgba(0,0,0,0.1);
}
.switch-wrap input:checked + .switch-track { background:var(--pink); }
.switch-wrap input:checked + .switch-track::after { left:22px; }

/* Add row */
.add-row {
  display:flex; align-items:center; justify-content:center; gap:6px;
  padding:14px; color:var(--pink); font-size:14px; cursor:pointer; font-weight:500;
}

/* Submit bar */
.submit-bar {
  position:fixed; bottom:0; left:0; right:0;
  padding:12px 16px; padding-bottom:calc(12px + env(safe-area-inset-bottom, 0px));
  background:var(--bg); z-index:10;
}
</style>
