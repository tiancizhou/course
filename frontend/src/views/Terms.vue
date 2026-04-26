<template>
  <div>
    <el-card shadow="hover">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <div style="font-size: 18px; font-weight: bold">学期管理</div>
        <el-button type="primary" @click="showAddDialog">创建学期</el-button>
      </div>

      <el-alert title="创建学期后，点击“一键生成课程”，系统会根据所有启用的固定时间段自动生成每周课程。" type="info" show-icon style="margin-bottom: 16px" />

      <el-table :data="terms" stripe>
        <el-table-column prop="name" label="学期名称" />
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : row.status === 'ended' ? 'info' : 'warning'" size="small">
              {{ statusMap[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="260">
          <template #default="{ row }">
            <el-button type="success" link size="small" @click="handleGenerate(row)">生成课程</el-button>
            <el-button type="primary" link size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑学期' : '创建学期'" width="500px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="学期名称"><el-input v-model="form.name" placeholder="如：2026春季班" /></el-form-item>
        <el-form-item label="开始日期"><el-date-picker v-model="form.start_date" value-format="YYYY-MM-DD" style="width: 100%" /></el-form-item>
        <el-form-item label="结束日期"><el-date-picker v-model="form.end_date" value-format="YYYY-MM-DD" style="width: 100%" /></el-form-item>
        <el-form-item label="状态" v-if="isEdit">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="未开始" value="not_started" />
            <el-option label="进行中" value="active" />
            <el-option label="已结束" value="ended" />
          </el-select>
        </el-form-item>
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
import { getTerms, createTerm, updateTerm, deleteTerm, generateLessons } from '@/api/terms'

const statusMap: Record<string, string> = { not_started: '未开始', active: '进行中', ended: '已结束' }
const terms = ref<any[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const form = ref<any>({ name: '', start_date: '', end_date: '', status: 'not_started', remark: '' })

async function loadData() {
  const res: any = await getTerms()
  terms.value = res.data
}

function showAddDialog() {
  isEdit.value = false
  editId.value = 0
  form.value = { name: '', start_date: '', end_date: '', status: 'not_started', remark: '' }
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
    await updateTerm(editId.value, form.value)
    ElMessage.success('更新成功')
  } else {
    await createTerm(form.value)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除学期「${row.name}」吗？`, '确认删除', { type: 'warning' })
  await deleteTerm(row.id)
  ElMessage.success('删除成功')
  loadData()
}

async function handleGenerate(row: any) {
  await ElMessageBox.confirm(`确定为「${row.name}」生成课程吗？重复课程会自动跳过。`, '生成课程', { type: 'info' })
  const res: any = await generateLessons(row.id)
  ElMessage.success(res.message || '生成成功')
  loadData()
}

onMounted(loadData)
</script>
