<template>
  <div class="manage">
    <div class="manage-header">
      <div class="mh-title">管理</div>
      <div class="mh-sub">学生 · 时间段 · 学期</div>
    </div>

    <div class="manage-grid">
      <div class="mg-item k-card" @click="$router.push('/students')" style="--c: var(--pink-soft);">
        <div class="mg-icon">👤</div>
        <span>学生管理</span>
      </div>
      <div class="mg-item k-card" @click="$router.push('/class-slots')" style="--c: var(--mint-soft);">
        <div class="mg-icon">🕐</div>
        <span>时间段</span>
      </div>
      <div class="mg-item k-card" @click="$router.push('/terms')" style="--c: var(--lavender-soft);">
        <div class="mg-icon">📅</div>
        <span>学期管理</span>
      </div>
    </div>

    <div class="k-section">快捷操作</div>
    <div class="manage-grid">
      <div class="mg-item k-card" @click="showAddStudent" style="--c: var(--cream-soft);">
        <div class="mg-icon">✨</div>
        <span>新增学生</span>
      </div>
      <div class="mg-item k-card" @click="loadTermsForGenerate" style="--c: var(--peach-soft);">
        <div class="mg-icon">📋</div>
        <span>生成课程</span>
      </div>
    </div>

    <!-- New student dialog -->
    <el-dialog v-model="studentDialog" title="新增学生" width="340px">
      <el-form :model="studentForm" label-position="top">
        <el-form-item label="学生姓名"><el-input v-model="studentForm.name" /></el-form-item>
        <el-form-item label="家长姓名"><el-input v-model="studentForm.parent_name" /></el-form-item>
        <el-form-item label="联系电话"><el-input v-model="studentForm.phone" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="studentForm.remark" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="studentDialog=false">取消</el-button>
        <el-button type="primary" @click="handleAddStudent">确定</el-button>
      </template>
    </el-dialog>

    <!-- Generate lessons dialog -->
    <el-dialog v-model="generateDialog" title="生成课程" width="340px">
      <el-form label-position="top">
        <el-form-item label="选择学期">
          <el-select v-model="selectedTermId" placeholder="请选择学期" style="width:100%">
            <el-option v-for="t in terms" :key="t.id" :label="`${t.name}（${t.start_date} ~ ${t.end_date}）`" :value="t.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="generateDialog=false">取消</el-button>
        <el-button type="primary" @click="handleGenerate" :disabled="!selectedTermId">生成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createStudent } from '@/api/students'
import { getTerms, generateLessons } from '@/api/terms'

// New student
const studentDialog = ref(false)
const studentForm = ref({ name: '', parent_name: '', phone: '', remark: '' })

function showAddStudent() {
  studentForm.value = { name: '', parent_name: '', phone: '', remark: '' }
  studentDialog.value = true
}

async function handleAddStudent() {
  if (!studentForm.value.name.trim()) { ElMessage.warning('请输入学生姓名'); return }
  await createStudent(studentForm.value)
  ElMessage.success('新增成功 ✓')
  studentDialog.value = false
}

// Generate lessons
const generateDialog = ref(false)
const terms = ref<any[]>([])
const selectedTermId = ref<number>()

async function loadTermsForGenerate() {
  const res: any = await getTerms()
  terms.value = res.data
  selectedTermId.value = undefined
  generateDialog.value = true
}

async function handleGenerate() {
  if (!selectedTermId.value) return
  await ElMessageBox.confirm('确认生成课程？重复课程会自动跳过', '生成课程', { type: 'info' })
  const res: any = await generateLessons(selectedTermId.value)
  ElMessage.success(res.message || '生成成功 ✓')
  generateDialog.value = false
}
</script>

<style scoped>
.manage { padding-bottom: 20px; }

.manage-header {
  text-align: center;
  padding: 8px 0 16px;
}
.mh-title { font-size: 22px; font-weight: 700; }
.mh-sub { font-size: 13px; color: var(--text-secondary); margin-top: 2px; }

.manage-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.mg-item {
  text-align: center;
  padding: 18px 8px;
  cursor: pointer;
  background: var(--c, var(--bg-card));
}

.mg-item:active { transform: scale(0.95); }

.mg-icon { font-size: 26px; margin-bottom: 6px; }
.mg-item span { font-size: 12px; font-weight: 600; color: var(--text-primary); }
</style>
