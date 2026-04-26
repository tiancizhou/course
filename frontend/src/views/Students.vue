<template>
  <div>
    <el-card shadow="hover">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <div style="font-size: 18px; font-weight: bold">学生管理</div>
        <div>
          <el-input v-model="keyword" placeholder="搜索学生姓名" style="width: 200px; margin-right: 10px" clearable @clear="loadData" @keyup.enter="loadData" />
          <el-select v-model="statusFilter" placeholder="状态筛选" style="width: 120px; margin-right: 10px" clearable @change="loadData">
            <el-option label="在读" value="active" />
            <el-option label="暂停" value="suspended" />
            <el-option label="退学" value="quit" />
          </el-select>
          <el-button type="primary" @click="showAddDialog">新增学生</el-button>
        </div>
      </div>

      <el-table :data="students" stripe>
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="parent_name" label="家长姓名" width="120" />
        <el-table-column prop="phone" label="电话" width="140" />
        <el-table-column label="剩余课时" width="100">
          <template #default="{ row }">
            <span :style="{ color: row.remaining_hours <= 3 ? '#f56c6c' : '#67c23a', fontWeight: 'bold' }">
              {{ row.remaining_hours }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : row.status === 'suspended' ? 'warning' : 'info'" size="small">
              {{ statusMap[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/students/${row.id}`)">详情</el-button>
            <el-button type="warning" link size="small" @click="showRechargeDialog(row)">充值</el-button>
            <el-button type="primary" link size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑学生' : '新增学生'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="学生姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="家长姓名">
          <el-input v-model="form.parent_name" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="状态" v-if="isEdit">
          <el-select v-model="form.status">
            <el-option label="在读" value="active" />
            <el-option label="暂停" value="suspended" />
            <el-option label="退学" value="quit" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 充值弹窗 -->
    <el-dialog v-model="rechargeVisible" title="充值课时" width="400px">
      <el-form :model="rechargeForm" label-width="80px">
        <el-form-item label="学生">
          <span>{{ currentStudent?.name }}</span>
          <span style="margin-left: 10px; color: #909399">当前剩余: {{ currentStudent?.remaining_hours }} 课时</span>
        </el-form-item>
        <el-form-item label="充值课时">
          <el-input-number v-model="rechargeForm.hours" :min="1" :max="999" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="rechargeForm.remark" placeholder="如：春季班续费 20 课时" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rechargeVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRecharge">确认充值</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getStudents, createStudent, updateStudent, deleteStudent, rechargeStudent } from '@/api/students'

const statusMap: Record<string, string> = { active: '在读', suspended: '暂停', quit: '退学' }

const students = ref<any[]>([])
const keyword = ref('')
const statusFilter = ref('')

// 新增/编辑
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const form = ref({ name: '', parent_name: '', phone: '', status: 'active', remark: '' })

// 充值
const rechargeVisible = ref(false)
const currentStudent = ref<any>(null)
const rechargeForm = ref({ hours: 20, remark: '' })

async function loadData() {
  const res: any = await getStudents({ keyword: keyword.value || undefined, status: statusFilter.value || undefined })
  students.value = res.data
}

function showAddDialog() {
  isEdit.value = false
  editId.value = 0
  form.value = { name: '', parent_name: '', phone: '', status: 'active', remark: '' }
  dialogVisible.value = true
}

function showEditDialog(row: any) {
  isEdit.value = true
  editId.value = row.id
  form.value = { name: row.name, parent_name: row.parent_name, phone: row.phone, status: row.status, remark: row.remark }
  dialogVisible.value = true
}

async function handleSubmit() {
  if (isEdit.value) {
    await updateStudent(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await createStudent(form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadData()
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除学生「${row.name}」吗？`, '确认删除', { type: 'warning' })
  await deleteStudent(row.id)
  ElMessage.success('删除成功')
  loadData()
}

function showRechargeDialog(row: any) {
  currentStudent.value = row
  rechargeForm.value = { hours: 20, remark: '' }
  rechargeVisible.value = true
}

async function handleRecharge() {
  if (!currentStudent.value) return
  await rechargeStudent(currentStudent.value.id, rechargeForm.value)
  ElMessage.success('充值成功')
  rechargeVisible.value = false
  loadData()
}

onMounted(loadData)
</script>
