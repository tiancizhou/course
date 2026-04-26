<template>
  <div class="lessons">
    <div class="filter-row">
      <el-date-picker v-model="filters.start_date" value-format="YYYY-MM-DD" placeholder="开始" size="small" style="flex:1" />
      <span style="color:var(--text-hint);margin:0 4px;font-size:12px">~</span>
      <el-date-picker v-model="filters.end_date" value-format="YYYY-MM-DD" placeholder="结束" size="small" style="flex:1" />
      <button class="k-btn k-btn-ghost" style="padding:6px 12px;font-size:12px;margin-left:6px" @click="loadData">查询</button>
    </div>
    <div class="filter-row" style="margin-top:6px">
      <div class="tab-pills">
        <span class="pill" :class="{active:!filters.status}" @click="filters.status='';loadData()">全部</span>
        <span class="pill" :class="{active:filters.status==='scheduled'}" @click="filters.status='scheduled';loadData()">待上课</span>
        <span class="pill" :class="{active:filters.status==='completed'}" @click="filters.status='completed';loadData()">已完成</span>
      </div>
      <button class="k-btn k-btn-mint" style="padding:6px 12px;font-size:12px;margin-left:auto" @click="showAdd=true">+ 临时课</button>
    </div>

    <div v-for="g in groupedLessons" :key="g.date" class="date-group">
      <div class="dg-label">{{ g.label }}</div>
      <div class="dg-card k-card" style="padding:0">
        <div v-for="l in g.items" :key="l.id" class="dg-item" @click="$router.push(`/lessons/${l.id}/attendance`)">
          <div class="dg-left">
            <div class="dg-time">{{ l.start_time?.slice(0,5) }}-{{ l.end_time?.slice(0,5) }}</div>
            <div class="dg-name">{{ l.slot_name || '临时课' }}</div>
          </div>
          <div class="dg-right">
            <span class="dg-count">{{ l.student_count }}人</span>
            <span class="lc-status" :class="l.status">{{ statusMap[l.status] }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="lessons.length===0" class="empty-card k-card"><div class="empty-text">暂无课程</div></div>

    <el-dialog v-model="showAdd" title="新增临时课" width="340px">
      <el-form :model="form" label-position="top">
        <el-form-item label="上课日期"><el-date-picker v-model="form.lesson_date" value-format="YYYY-MM-DD" style="width:100%" @change="updateWeekday" /></el-form-item>
        <el-form-item label="开始时间"><el-time-picker v-model="form.start_time" value-format="HH:mm:ss" format="HH:mm" style="width:100%" /></el-form-item>
        <el-form-item label="结束时间"><el-time-picker v-model="form.end_time" value-format="HH:mm:ss" format="HH:mm" style="width:100%" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAdd=false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getLessons, createLesson } from '@/api/lessons'

const weekdayNames = ['周一','周二','周三','周四','周五','周六','周日']
const statusMap: Record<string,string> = { scheduled:'待上课', completed:'已完成', cancelled:'已取消' }

const lessons = ref<any[]>([])
const filters = ref<any>({ start_date:'', end_date:'', status:'' })
const showAdd = ref(false)
const form = ref<any>({ lesson_date:'', weekday:0, start_time:'09:00:00', end_time:'10:30:00', remark:'' })

const groupedLessons = computed(() => {
  const map = new Map<string,any[]>()
  for (const l of lessons.value) {
    if (!map.has(l.lesson_date)) map.set(l.lesson_date, [])
    map.get(l.lesson_date)!.push(l)
  }
  return Array.from(map.entries()).map(([date,items]) => ({
    date, label:`${date} ${weekdayNames[items[0]?.weekday??0]}`, items
  }))
})

async function loadData() {
  const params:any = {}
  Object.keys(filters.value).forEach(k=>{ if(filters.value[k]) params[k]=filters.value[k] })
  const res:any = await getLessons(params); lessons.value = res.data
}

function updateWeekday() { if(!form.value.lesson_date) return; const d=new Date(form.value.lesson_date); form.value.weekday=(d.getDay()+6)%7 }

async function handleAdd() {
  await createLesson(form.value); ElMessage.success('新增成功 ✓'); showAdd.value=false; loadData()
}

onMounted(loadData)
</script>

<style scoped>
.lessons { padding-bottom:16px; }

.filter-row { display:flex; align-items:center; }

.tab-pills { display:flex; gap:6px; }
.pill {
  padding:5px 12px; border-radius:20px; font-size:12px; font-weight:500;
  color:var(--text-secondary); background:var(--bg-card); cursor:pointer;
  transition:all 0.2s; border:1.5px solid transparent;
}
.pill.active { background:var(--pink-soft); color:var(--pink); border-color:var(--pink); }

.date-group { margin-top:14px; }
.dg-label { font-size:13px; color:var(--text-secondary); font-weight:600; margin-bottom:6px; }
.dg-card { overflow:hidden; }
.dg-item { display:flex; justify-content:space-between; align-items:center; padding:12px 16px; border-bottom:1px solid #F5F2F8; cursor:pointer; }
.dg-item:last-child { border-bottom:none; }
.dg-item:active { background:#FAF7FD; }
.dg-time { font-size:12px; color:var(--text-hint); }
.dg-name { font-size:14px; font-weight:500; margin-top:1px; }
.dg-right { display:flex; align-items:center; gap:6px; }
.dg-count { font-size:11px; color:var(--text-hint); }

.lc-status { font-size:11px; padding:3px 8px; border-radius:8px; font-weight:500; }
.lc-status.scheduled { background:var(--cream-soft); color:#B8941E; }
.lc-status.completed { background:var(--mint-soft); color:#4AA898; }
.lc-status.cancelled { background:#f2f2f5; color:#aaa; }

.empty-card { text-align:center; padding:28px; margin-top:14px; }
.empty-text { color:var(--text-hint); font-size:14px; }
</style>
