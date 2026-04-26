<template>
  <div class="students">
    <div class="k-top">
      <button class="k-top-back" @click="$router.back()">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>
        返回
      </button>
      <span class="k-top-title">学生管理</span>
      <button class="k-btn k-btn-pink" style="padding:6px 14px;font-size:12px" @click="showAddDialog">+ 新增</button>
    </div>

    <div class="search-row">
      <el-input v-model="keyword" placeholder="搜索姓名" clearable size="small" @clear="loadData" @keyup.enter="loadData" />
      <el-select v-model="statusFilter" placeholder="状态" clearable size="small" @change="loadData" style="width:80px">
        <el-option label="在读" value="active" /><el-option label="暂停" value="suspended" /><el-option label="退学" value="quit" />
      </el-select>
    </div>

    <div class="stu-list">
      <div v-for="s in students" :key="s.id" class="stu-card k-card" @click="$router.push(`/students/${s.id}`)">
        <div class="sc-top">
          <span class="sc-name">{{ s.name }}</span>
          <span class="sc-badge" :class="s.status">{{ statusMap[s.status] }}</span>
        </div>
        <div class="sc-mid">
          <span>{{ s.phone || '未填电话' }}</span>
          <span class="sc-hours" :class="{low: s.remaining_hours <= 3}">{{ s.remaining_hours }} 课时</span>
        </div>
        <div class="sc-btns" @click.stop>
          <button class="k-btn k-btn-cream" style="padding:4px 12px;font-size:12px" @click="showRechargeDialog(s)">充值</button>
          <button class="k-btn k-btn-ghost" style="padding:4px 12px;font-size:12px" @click="showEditDialog(s)">编辑</button>
          <button class="k-btn" style="padding:4px 12px;font-size:12px;background:var(--bg-pink);color:var(--pink)" @click="handleDelete(s)">删除</button>
        </div>
      </div>
    </div>

    <div v-if="students.length===0" class="empty-card k-card"><div class="empty-text">暂无学生</div></div>

    <el-dialog v-model="dialogVisible" :title="isEdit?'编辑学生':'新增学生'" width="340px">
      <el-form :model="form" label-position="top">
        <el-form-item label="学生姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="家长姓名"><el-input v-model="form.parent_name" /></el-form-item>
        <el-form-item label="联系电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="状态" v-if="isEdit">
          <el-select v-model="form.status" style="width:100%"><el-option label="在读" value="active" /><el-option label="暂停" value="suspended" /><el-option label="退学" value="quit" /></el-select>
        </el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="rechargeVisible" title="充值课时" width="340px">
      <el-form :model="rechargeForm" label-position="top">
        <el-form-item :label="`${currentStudent?.name}（当前 ${currentStudent?.remaining_hours} 课时）`">
          <el-input-number v-model="rechargeForm.hours" :min="1" :max="999" style="width:100%" />
        </el-form-item>
        <el-form-item label="备注"><el-input v-model="rechargeForm.remark" placeholder="如：续费 20 课时" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rechargeVisible=false">取消</el-button>
        <el-button type="primary" @click="handleRecharge">确认充值</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getStudents, createStudent, updateStudent, deleteStudent, rechargeStudent } from '@/api/students'

const statusMap: Record<string,string> = { active:'在读', suspended:'暂停', quit:'退学' }
const students = ref<any[]>([])
const keyword = ref(''), statusFilter = ref('')
const dialogVisible = ref(false), isEdit = ref(false), editId = ref(0)
const form = ref({ name:'', parent_name:'', phone:'', status:'active', remark:'' })
const rechargeVisible = ref(false), currentStudent = ref<any>(null)
const rechargeForm = ref({ hours:20, remark:'' })

async function loadData() { const r:any = await getStudents({ keyword:keyword.value||undefined, status:statusFilter.value||undefined }); students.value = r.data }
function showAddDialog() { isEdit.value=false; editId.value=0; form.value={name:'',parent_name:'',phone:'',status:'active',remark:''}; dialogVisible.value=true }
function showEditDialog(row:any) { isEdit.value=true; editId.value=row.id; form.value={name:row.name,parent_name:row.parent_name,phone:row.phone,status:row.status,remark:row.remark}; dialogVisible.value=true }
async function handleSubmit() { if(isEdit.value){await updateStudent(editId.value,form.value)}else{await createStudent(form.value)}; ElMessage.success('成功 ✓'); dialogVisible.value=false; loadData() }
async function handleDelete(row:any) { await ElMessageBox.confirm(`删除学生「${row.name}」？`,'确认',{type:'warning'}); await deleteStudent(row.id); ElMessage.success('删除成功'); loadData() }
function showRechargeDialog(row:any) { currentStudent.value=row; rechargeForm.value={hours:20,remark:''}; rechargeVisible.value=true }
async function handleRecharge() { if(!currentStudent.value) return; await rechargeStudent(currentStudent.value.id,rechargeForm.value); ElMessage.success('充值成功 ✓'); rechargeVisible.value=false; loadData() }
onMounted(loadData)
</script>

<style scoped>
.students { padding-bottom:16px; }
.search-row { display:flex; gap:8px; margin-bottom:12px; }
.stu-list { display:flex; flex-direction:column; gap:8px; }
.stu-card { cursor:pointer; }
.stu-card:active { transform:scale(0.98); }
.sc-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }
.sc-name { font-size:15px; font-weight:600; }
.sc-badge { font-size:11px; padding:2px 8px; border-radius:8px; font-weight:500; }
.sc-badge.active { background:var(--mint-soft); color:#4AA898; }
.sc-badge.suspended { background:var(--cream-soft); color:#B8941E; }
.sc-badge.quit { background:#f2f2f5; color:#aaa; }
.sc-mid { display:flex; justify-content:space-between; font-size:13px; color:var(--text-secondary); margin-bottom:10px; }
.sc-hours { font-weight:700; }
.sc-hours.low { color:#D4647A; }
.sc-btns { display:flex; gap:6px; }
.empty-card { text-align:center; padding:28px; }
.empty-text { color:var(--text-hint); font-size:14px; }
</style>
