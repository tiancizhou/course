<template>
  <div class="terms">
    <div class="k-top">
      <button class="k-top-back" @click="$router.back()">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>
        返回
      </button>
      <span class="k-top-title">学期管理</span>
      <button class="k-btn k-btn-pink" style="padding:6px 14px;font-size:12px" @click="showAddDialog">+ 新增</button>
    </div>

    <div class="hint-card k-card" style="background:var(--bg-lavender)">
      <div class="hint-text">创建学期后，点击「生成课程」自动排课</div>
    </div>

    <div class="term-list">
      <div v-for="t in terms" :key="t.id" class="term-card k-card">
        <div class="tc-top">
          <span class="tc-name">{{ t.name }}</span>
          <span class="tc-badge" :class="t.status">{{ statusMap[t.status] }}</span>
        </div>
        <div class="tc-dates">{{ t.start_date }} ~ {{ t.end_date }}</div>
        <div class="tc-btns">
          <button class="k-btn k-btn-mint" style="padding:4px 12px;font-size:12px" @click="handleGenerate(t)">生成课程</button>
          <button class="k-btn k-btn-ghost" style="padding:4px 12px;font-size:12px" @click="showEditDialog(t)">编辑</button>
          <button class="k-btn" style="padding:4px 12px;font-size:12px;background:var(--bg-pink);color:var(--pink)" @click="handleDelete(t)">删除</button>
        </div>
      </div>
    </div>

    <div v-if="terms.length===0" class="empty-card k-card"><div class="empty-text">暂无学期</div></div>

    <el-dialog v-model="dialogVisible" :title="isEdit?'编辑学期':'创建学期'" width="340px">
      <el-form :model="form" label-position="top">
        <el-form-item label="学期名称"><el-input v-model="form.name" placeholder="如：2026春季班" /></el-form-item>
        <el-form-item label="开始日期"><el-date-picker v-model="form.start_date" value-format="YYYY-MM-DD" style="width:100%" /></el-form-item>
        <el-form-item label="结束日期"><el-date-picker v-model="form.end_date" value-format="YYYY-MM-DD" style="width:100%" /></el-form-item>
        <el-form-item label="状态" v-if="isEdit"><el-select v-model="form.status" style="width:100%"><el-option label="未开始" value="not_started" /><el-option label="进行中" value="active" /><el-option label="已结束" value="ended" /></el-select></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTerms, createTerm, updateTerm, deleteTerm, generateLessons } from '@/api/terms'

const statusMap: Record<string,string> = { not_started:'未开始', active:'进行中', ended:'已结束' }
const terms = ref<any[]>([])
const dialogVisible = ref(false), isEdit = ref(false), editId = ref(0)
const form = ref<any>({name:'',start_date:'',end_date:'',status:'not_started',remark:''})

async function loadData() { const r:any = await getTerms(); terms.value = r.data }
function showAddDialog() { isEdit.value=false; editId.value=0; form.value={name:'',start_date:'',end_date:'',status:'not_started',remark:''}; dialogVisible.value=true }
function showEditDialog(row:any) { isEdit.value=true; editId.value=row.id; form.value={...row}; dialogVisible.value=true }
async function handleSubmit() { if(isEdit.value){await updateTerm(editId.value,form.value)}else{await createTerm(form.value)}; ElMessage.success('成功 ✓'); dialogVisible.value=false; loadData() }
async function handleDelete(row:any) { await ElMessageBox.confirm(`删除「${row.name}」？`,'确认',{type:'warning'}); await deleteTerm(row.id); ElMessage.success('删除成功'); loadData() }
async function handleGenerate(row:any) { await ElMessageBox.confirm(`为「${row.name}」生成课程？`,'生成课程',{type:'info'}); const r:any = await generateLessons(row.id); ElMessage.success(r.message||'生成成功 ✓'); loadData() }
onMounted(loadData)
</script>

<style scoped>
.terms { padding-bottom:16px; }

.hint-card { margin-bottom:12px; }
.hint-text { font-size:13px; color:var(--lavender); font-weight:500; }

.term-list { display:flex; flex-direction:column; gap:8px; margin-top:10px; }
.tc-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }
.tc-name { font-size:15px; font-weight:600; }
.tc-badge { font-size:11px; padding:3px 8px; border-radius:8px; font-weight:500; }
.tc-badge.not_started { background:var(--cream-soft); color:#B8941E; }
.tc-badge.active { background:var(--mint-soft); color:#4AA898; }
.tc-badge.ended { background:#f2f2f5; color:#aaa; }
.tc-dates { font-size:13px; color:var(--text-secondary); margin-bottom:10px; }
.tc-btns { display:flex; gap:6px; }

.empty-card { text-align:center; padding:28px; }
.empty-text { color:var(--text-hint); font-size:14px; }
</style>
