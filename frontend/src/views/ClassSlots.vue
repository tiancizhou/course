<template>
  <div>
    <el-card shadow="hover">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <div style="font-size: 18px; font-weight: bold">固定时间段</div>
        <el-button type="primary" @click="showAddDialog">新增时间段</el-button>
      </div>

      <el-table :data="slots" stripe row-key="id">
        <el-table-column type="expand">
          <template #default="{ row }">
            <div style="padding: 10px 40px">
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px">
                <b>班级学生</b>
                <el-button type="primary" size="small" @click="showAddStudentDialog(row)">添加学生</el-button>
              </div>
              <el-table :data="(row.students || []).filter((s: any) => s.status === 'active')" size="small">
                <el-table-column prop="student_name" label="学生姓名" />
                <el-table-column prop="start_date" label="加入日期" />
                <el-table-column label="操作" width="100">
                  <template #default="{ row: stu }">
                    <el-button type="danger" link size="small" @click="handleRemoveStudent(row, stu)">移除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" />
        <el-table-column label="星期" width="100">
          <template #default="{ row }">{{ weekdayNames[row.weekday] }}</template>
        </el-table-column>
        <el-table-column label="时间" width="160">
          <template #default="{ row }">{{ row.start_time }} - {{ row.end_time }}</template>
        </el-table-column>
        <el-table-column prop="location" label="地点" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'" size="small">{{ row.is_active ? '启用' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑时间段' : '新增时间段'" width="500px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="名称"><el-input v-model="form.name" placeholder="如：周六上午班" /></el-form-item>
        <el-form-item label="星期">
          <el-select v-model="form.weekday" style="width: 100%">
            <el-option v-for="(name, idx) in weekdayNames" :key="idx" :label="name" :value="idx" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间"><el-time-picker v-model="form.start_time" value-format="HH:mm:ss" format="HH:mm" style="width: 100%" /></el-form-item>
        <el-form-item label="结束时间"><el-time-picker v-model="form.end_time" value-format="HH:mm:ss" format="HH:mm" style="width: 100%" /></el-form-item>
        <el-form-item label="地点"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="是否启用" v-if="isEdit"><el-switch v-model="form.is_active" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="studentDialogVisible" title="添加学生到时间段" width="400px">
      <el-form :model="slotStudentForm" label-width="90px">
        <el-form-item label="时间段">{{ currentSlot?.name }}</el-form-item>
        <el-form-item label="学生">
          <el-select v-model="slotStudentForm.student_id" filterable style="width: 100%">
            <el-option v-for="s in students" :key="s.id" :label="`${s.name}（剩余 ${s.remaining_hours}）`" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="生效日期">
          <el-date-picker v-model="slotStudentForm.start_date" value-format="YYYY-MM-DD" style="width: 100%" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { getClassSlots, createClassSlot, updateClassSlot, deleteClassSlot, addSlotStudent, removeSlotStudent } from '@/api/classSlots'
import { getStudents } from '@/api/students'

const weekdayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const slots = ref<any[]>([])
const students = ref<any[]>([])
const dialogVisible = ref(false)
const studentDialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const currentSlot = ref<any>(null)
const form = ref<any>({ name: '', weekday: 5, start_time: '09:00:00', end_time: '10:30:00', location: '', is_active: true, remark: '' })
const slotStudentForm = ref<any>({ student_id: undefined, start_date: new Date().toISOString().slice(0, 10) })

async function loadData() {
  const [slotsRes, studentsRes]: any[] = await Promise.all([getClassSlots(), getStudents({ status: 'active' })])
  slots.value = slotsRes.data
  students.value = studentsRes.data
}

function showAddDialog() {
  isEdit.value = false
  editId.value = 0
  form.value = { name: '', weekday: 5, start_time: '09:00:00', end_time: '10:30:00', location: '', is_active: true, remark: '' }
  dialogVisible.value = true
}

function showEditDialog(row: any) {
  isEdit.value = true
  editId.value = row.id
  form.value = { ...row }
  dialogVisible.value = true
}

async function handleSubmit() {
  if (isEdit.value) {
    await updateClassSlot(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await createClassSlot(form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadData()
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除时间段「${row.name}」吗？`, '确认删除', { type: 'warning' })
  await deleteClassSlot(row.id)
  ElMessage.success('删除成功')
  loadData()
}

function showAddStudentDialog(row: any) {
  currentSlot.value = row
  slotStudentForm.value = { student_id: undefined, start_date: new Date().toISOString().slice(0, 10) }
  studentDialogVisible.value = true
}

async function handleAddStudent() {
  if (!currentSlot.value) return
  await addSlotStudent(currentSlot.value.id, slotStudentForm.value)
  ElMessage.success('添加成功')
  studentDialogVisible.value = false
  loadData()
}

async function handleRemoveStudent(slot: any, stu: any) {
  await ElMessageBox.confirm(`确定从「${slot.name}」移除学生「${stu.student_name}」吗？`, '确认移除', { type: 'warning' })
  await removeSlotStudent(slot.id, stu.student_id)
  ElMessage.success('移除成功')
  loadData()
}

onMounted(loadData)
</script>
