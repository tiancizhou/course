<template>
  <div>
    <el-card shadow="hover">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <div style="font-size: 18px; font-weight: bold">课程管理</div>
        <el-button type="primary" @click="showAddDialog">新增临时课</el-button>
      </div>

      <div style="margin-bottom: 16px">
        <el-date-picker v-model="filters.start_date" value-format="YYYY-MM-DD" placeholder="开始日期" style="width: 160px; margin-right: 8px" />
        <el-date-picker v-model="filters.end_date" value-format="YYYY-MM-DD" placeholder="结束日期" style="width: 160px; margin-right: 8px" />
        <el-select v-model="filters.status" placeholder="状态" clearable style="width: 120px; margin-right: 8px">
          <el-option label="待上课" value="scheduled" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
        <el-button type="primary" @click="loadData">筛选</el-button>
        <el-button @click="resetFilters">重置</el-button>
      </div>

      <el-table :data="lessons" stripe>
        <el-table-column label="日期" width="150">
          <template #default="{ row }">{{ row.lesson_date }} {{ weekdayNames[row.weekday] }}</template>
        </el-table-column>
        <el-table-column prop="slot_name" label="班级/时间段" />
        <el-table-column label="时间" width="160">
          <template #default="{ row }">{{ row.start_time }} - {{ row.end_time }}</template>
        </el-table-column>
        <el-table-column label="类型" width="100">
          <template #default="{ row }"><el-tag size="small">{{ typeMap[row.lesson_type] }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="student_count" label="学生数" width="80" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : row.status === 'cancelled' ? 'info' : 'warning'" size="small">
              {{ statusMap[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="220">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/lessons/${row.id}/attendance`)">点名</el-button>
            <el-button type="primary" link size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑课程' : '新增临时课'" width="500px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="上课日期"><el-date-picker v-model="form.lesson_date" value-format="YYYY-MM-DD" style="width: 100%" @change="updateWeekday" /></el-form-item>
        <el-form-item label="星期"><el-select v-model="form.weekday" style="width: 100%"><el-option v-for="(name, idx) in weekdayNames" :key="idx" :label="name" :value="idx" /></el-select></el-form-item>
        <el-form-item label="开始时间"><el-time-picker v-model="form.start_time" value-format="HH:mm:ss" format="HH:mm" style="width: 100%" /></el-form-item>
        <el-form-item label="结束时间"><el-time-picker v-model="form.end_time" value-format="HH:mm:ss" format="HH:mm" style="width: 100%" /></el-form-item>
        <el-form-item label="状态" v-if="isEdit"><el-select v-model="form.status" style="width: 100%"><el-option label="待上课" value="scheduled" /><el-option label="已完成" value="completed" /><el-option label="已取消" value="cancelled" /></el-select></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getLessons, createLesson, updateLesson, deleteLesson } from '@/api/lessons'

const weekdayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const statusMap: Record<string, string> = { scheduled: '待上课', completed: '已完成', cancelled: '已取消' }
const typeMap: Record<string, string> = { regular: '固定课', makeup: '补课', temporary: '临时课' }
const lessons = ref<any[]>([])
const filters = ref<any>({ start_date: '', end_date: '', status: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const form = ref<any>({ lesson_date: '', weekday: 0, start_time: '09:00:00', end_time: '10:30:00', lesson_type: 'temporary', status: 'scheduled', remark: '' })

async function loadData() {
  const params: any = {}
  Object.keys(filters.value).forEach(k => { if (filters.value[k]) params[k] = filters.value[k] })
  const res: any = await getLessons(params)
  lessons.value = res.data
}

function resetFilters() {
  filters.value = { start_date: '', end_date: '', status: '' }
  loadData()
}

function showAddDialog() {
  isEdit.value = false
  editId.value = 0
  form.value = { lesson_date: '', weekday: 0, start_time: '09:00:00', end_time: '10:30:00', lesson_type: 'temporary', status: 'scheduled', remark: '' }
  dialogVisible.value = true
}

function showEditDialog(row: any) {
  isEdit.value = true
  editId.value = row.id
  form.value = { ...row }
  dialogVisible.value = true
}

function updateWeekday() {
  if (!form.value.lesson_date) return
  const d = new Date(form.value.lesson_date)
  form.value.weekday = (d.getDay() + 6) % 7
}

async function handleSubmit() {
  if (isEdit.value) {
    await updateLesson(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await createLesson(form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadData()
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除这节课程吗？`, '确认删除', { type: 'warning' })
  await deleteLesson(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>
