<template>
  <div>
    <el-card shadow="hover" style="margin-bottom: 20px">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <div style="font-size: 18px; font-weight: bold">课程点名</div>
        <el-button @click="$router.back()">返回</el-button>
      </div>
      <el-descriptions v-if="lesson" :column="3" border>
        <el-descriptions-item label="课程日期">{{ lesson.lesson_date }} {{ weekdayNames[lesson.weekday] }}</el-descriptions-item>
        <el-descriptions-item label="时间">{{ lesson.start_time }} - {{ lesson.end_time }}</el-descriptions-item>
        <el-descriptions-item label="班级">{{ lesson.slot_name || '临时课' }}</el-descriptions-item>
        <el-descriptions-item label="类型">{{ typeMap[lesson.lesson_type] }}</el-descriptions-item>
        <el-descriptions-item label="状态">{{ statusMap[lesson.status] }}</el-descriptions-item>
        <el-descriptions-item label="备注">{{ lesson.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card shadow="hover">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <div style="font-size: 16px; font-weight: bold">学生点名</div>
        <div>
          <el-button @click="showAddStudentDialog">添加学生</el-button>
          <el-button type="primary" @click="handleSubmitAttendance">提交点名并扣课时</el-button>
        </div>
      </div>

      <el-alert title="重复提交点名时，系统会先回滚本节课之前扣过的课时，再按当前点名结果重新扣课时。" type="info" show-icon style="margin-bottom: 16px" />

      <el-table :data="lessonStudents" stripe>
        <el-table-column prop="student_name" label="学生姓名" width="120" />
        <el-table-column label="来源" width="90">
          <template #default="{ row }">{{ sourceMap[row.source_type] }}</template>
        </el-table-column>
        <el-table-column label="点名状态" width="220">
          <template #default="{ row }">
            <el-radio-group v-model="row.attendance_status" @change="handleStatusChange(row)">
              <el-radio-button label="present">到课</el-radio-button>
              <el-radio-button label="leave">请假</el-radio-button>
              <el-radio-button label="absent">缺席</el-radio-button>
              <el-radio-button label="makeup">补课</el-radio-button>
            </el-radio-group>
          </template>
        </el-table-column>
        <el-table-column label="扣课时" width="140">
          <template #default="{ row }">
            <el-input-number v-model="row.deduct_hours" :min="0" :max="5" :step="1" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="上次变化" width="100">
          <template #default="{ row }">
            <span :style="{ color: Number(row.hour_change) < 0 ? '#f56c6c' : '#909399' }">{{ row.hour_change }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" />
        <el-table-column label="操作" width="90">
          <template #default="{ row }">
            <el-button type="danger" link size="small" @click="handleRemoveStudent(row)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="studentDialogVisible" title="添加学生到本节课" width="400px">
      <el-form :model="addStudentForm" label-width="80px">
        <el-form-item label="学生">
          <el-select v-model="addStudentForm.student_id" filterable style="width: 100%">
            <el-option v-for="s in allStudents" :key="s.id" :label="`${s.name}（剩余 ${s.remaining_hours}）`" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="来源">
          <el-select v-model="addStudentForm.source_type" style="width: 100%">
            <el-option label="手动添加" value="manual" />
            <el-option label="补课" value="makeup" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="studentDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddStudent">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getLesson, getLessonStudents, addLessonStudent, removeLessonStudent, takeAttendance } from '@/api/lessons'
import { getStudents } from '@/api/students'

const route = useRoute()
const lessonId = Number(route.params.id)
const lesson = ref<any>(null)
const lessonStudents = ref<any[]>([])
const allStudents = ref<any[]>([])
const studentDialogVisible = ref(false)
const addStudentForm = ref<any>({ student_id: undefined, source_type: 'manual' })

const weekdayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const statusMap: Record<string, string> = { scheduled: '待上课', completed: '已完成', cancelled: '已取消' }
const typeMap: Record<string, string> = { regular: '固定课', makeup: '补课', temporary: '临时课' }
const sourceMap: Record<string, string> = { slot: '固定班', manual: '手动', makeup: '补课' }

async function loadData() {
  const [lessonRes, studentsRes, allStudentsRes]: any[] = await Promise.all([
    getLesson(lessonId),
    getLessonStudents(lessonId),
    getStudents({ status: 'active' }),
  ])
  lesson.value = lessonRes.data
  lessonStudents.value = studentsRes.data.map((s: any) => ({
    ...s,
    attendance_status: s.attendance_status === 'pending' ? 'present' : s.attendance_status,
    deduct_hours: Number(s.hour_change) < 0 ? Math.abs(Number(s.hour_change)) : defaultDeduct(s.attendance_status),
  }))
  allStudents.value = allStudentsRes.data
}

function defaultDeduct(status: string) {
  if (status === 'leave') return 0
  return 1
}

function handleStatusChange(row: any) {
  row.deduct_hours = row.attendance_status === 'leave' ? 0 : 1
}

function showAddStudentDialog() {
  addStudentForm.value = { student_id: undefined, source_type: 'manual' }
  studentDialogVisible.value = true
}

async function handleAddStudent() {
  await addLessonStudent(lessonId, addStudentForm.value)
  ElMessage.success('添加成功')
  studentDialogVisible.value = false
  loadData()
}

async function handleRemoveStudent(row: any) {
  await ElMessageBox.confirm(`确定从本节课移除「${row.student_name}」吗？`, '确认移除', { type: 'warning' })
  await removeLessonStudent(lessonId, row.student_id)
  ElMessage.success('移除成功')
  loadData()
}

async function handleSubmitAttendance() {
  const records = lessonStudents.value.map(s => ({
    student_id: s.student_id,
    attendance_status: s.attendance_status,
    deduct_hours: Number(s.deduct_hours || 0),
  }))
  await takeAttendance(lessonId, records)
  ElMessage.success('点名成功，课时已更新')
  loadData()
}

onMounted(loadData)
</script>
