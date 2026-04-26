<template>
  <div class="slots">
    <div class="k-top">
      <button class="k-top-back" @click="$router.back()">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>
        返回
      </button>
      <span class="k-top-title">固定时间段</span>
      <button class="k-btn k-btn-mint" style="padding:6px 14px;font-size:12px" @click="showAddDialog">+ 新增</button>
    </div>

    <div class="slot-list">
      <div v-for="s in slots" :key="s.id" class="slot-card k-card">
        <div class="sl-header" @click="toggle(s.id)">
          <div>
            <div class="sl-name">{{ s.name }}</div>
            <div class="sl-meta">{{ weekdayNames[s.weekday] }} {{ s.start_time?.slice(0,5) }}-{{ s.end_time?.slice(0,5) }}</div>
          </div>
          <span class="sl-tag" :class="{on:s.is_active}">{{ s.is_active?'启用':'停用' }}</span>
        </div>
        <div v-if="expandedId===s.id" class="sl-expand">
          <div class="chips">
            <span v-for="ss in (s.students||[]).filter((x:any)=>x.status==='active')" :key="ss.id" class="chip">
              {{ ss.student_name }}
              <span class="chip-x" @click="handleRemove(s,ss)">&times;</span>
            </span>
            <span class="chip chip-add" @click="openAddStudent(s)">+ 添加</span>
          </div>
          <div class="sl-acts">
            <button class="k-btn k-btn-ghost" style="padding:4px 12px;font-size:12px" @click="showEditDialog(s)">编辑</button>
            <button class="k-btn" style="padding:4px 12px;font-size:12px;background:var(--bg-pink);color:var(--pink)" @click="handleDelete(s)">删除</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="slots.length===0" class="empty-card k-card"><div class="empty-text">暂无时间段</div></div>

    <el-dialog v-model="dialogVisible" :title="isEdit?'编辑时间段':'新增时间段'" width="340px">
      <el-form :model="form" label-position="top">
        <el-form-item label="名称"><el-input v-model="form.name" placeholder="如：周六上午班" /></el-form-item>
        <el-form-item label="星期"><el-select v-model="form.weekday" style="width:100%"><el-option v-for="(n,i) in weekdayNames" :key="i" :label="n" :value="i" /></el-select></el-form-item>
        <el-form-item label="开始时间"><el-time-picker v-model="form.start_time" value-format="HH:mm:ss" format="HH:mm" style="width:100%" /></el-form-item>
        <el-form-item label="结束时间"><el-time-picker v-model="form.end_time" value-format="HH:mm:ss" format="HH:mm" style="width:100%" /></el-form-item>
        <el-form-item label="地点"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="启用" v-if="isEdit"><el-switch v-model="form.is_active" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="stuDialog" title="添加学生" width="340px">
      <el-form label-position="top">
        <el-form-item label="学生"><el-select v-model="ssf.student_id" filterable placeholder="搜索" style="width:100%"><el-option v-for="s in allStudents" :key="s.id" :label="`${s.name}（${s.remaining_hours}）`" :value="s.id" /></el-select></el-form-item>
        <el-form-item label="生效日期"><el-date-picker v-model="ssf.start_date" value-format="YYYY-MM-DD" style="width:100%" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="stuDialog=false">取消</el-button>
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

const weekdayNames = ['周一','周二','周三','周四','周五','周六','周日']
const slots = ref<any[]>([])
const allStudents = ref<any[]>([])
const expandedId = ref(0)
const dialogVisible = ref(false), isEdit = ref(false), editId = ref(0)
const form = ref<any>({name:'',weekday:5,start_time:'09:00:00',end_time:'10:30:00',location:'',is_active:true,remark:''})
const stuDialog = ref(false), curSlot = ref<any>(null)
const ssf = ref<any>({student_id:undefined,start_date:new Date().toISOString().slice(0,10)})

function toggle(id:number) { expandedId.value = expandedId.value===id?0:id }
async function loadData() { const [sr,ar]:any[] = await Promise.all([getClassSlots(),getStudents({status:'active'})]); slots.value=sr.data; allStudents.value=ar.data }
function showAddDialog() { isEdit.value=false; editId.value=0; form.value={name:'',weekday:5,start_time:'09:00:00',end_time:'10:30:00',location:'',is_active:true,remark:''}; dialogVisible.value=true }
function showEditDialog(row:any) { isEdit.value=true; editId.value=row.id; form.value={...row}; dialogVisible.value=true }
async function handleSubmit() { if(isEdit.value){await updateClassSlot(editId.value,form.value)}else{await createClassSlot(form.value)}; ElMessage.success('成功 ✓'); dialogVisible.value=false; loadData() }
async function handleDelete(row:any) { await ElMessageBox.confirm(`删除「${row.name}」？`,'确认',{type:'warning'}); await deleteClassSlot(row.id); ElMessage.success('删除成功'); loadData() }
function openAddStudent(row:any) { curSlot.value=row; ssf.value={student_id:undefined,start_date:new Date().toISOString().slice(0,10)}; stuDialog.value=true }
async function handleAddStudent() { await addSlotStudent(curSlot.value.id,ssf.value); ElMessage.success('添加成功 ✓'); stuDialog.value=false; loadData() }
async function handleRemove(slot:any,stu:any) { await ElMessageBox.confirm(`移除「${stu.student_name}」？`,'确认',{type:'warning'}); await removeSlotStudent(slot.id,stu.student_id); ElMessage.success('移除成功'); loadData() }
onMounted(loadData)
</script>

<style scoped>
.slots { padding-bottom:16px; }
.slot-list { display:flex; flex-direction:column; gap:8px; }

.sl-header { display:flex; justify-content:space-between; align-items:center; cursor:pointer; }
.sl-header:active { opacity:0.8; }
.sl-name { font-size:15px; font-weight:600; }
.sl-meta { font-size:12px; color:var(--text-secondary); margin-top:2px; }
.sl-tag { font-size:11px; padding:3px 8px; border-radius:8px; font-weight:500; }
.sl-tag.on { background:var(--mint-soft); color:#4AA898; }
.sl-tag { background:#f2f2f5; color:#aaa; }

.sl-expand { margin-top:10px; padding-top:10px; border-top:1px solid #F5F2F8; }
.chips { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }
.chip { background:var(--lavender-soft); color:var(--lavender); padding:4px 10px; border-radius:14px; font-size:12px; display:flex; align-items:center; gap:4px; }
.chip-x { cursor:pointer; font-size:14px; }
.chip-add { background:var(--bg-mint); color:var(--mint); cursor:pointer; }
.sl-acts { display:flex; gap:6px; }

.empty-card { text-align:center; padding:28px; }
.empty-text { color:var(--text-hint); font-size:14px; }
</style>
