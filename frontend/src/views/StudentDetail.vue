<template>
  <div class="detail" v-if="student">
    <div class="k-top">
      <button class="k-top-back" @click="$router.back()">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>
        返回
      </button>
      <span class="k-top-title">{{ student.name }}</span>
      <button class="k-btn k-btn-cream" style="padding:6px 14px;font-size:12px" @click="rechargeVisible=true">充值</button>
    </div>

    <div class="info-card k-card">
      <div class="ir" v-for="item in infoItems" :key="item.label">
        <span class="ir-label">{{ item.label }}</span>
        <span class="ir-value" :class="item.cls">{{ item.value }}</span>
      </div>
    </div>

    <div class="k-section">课时流水</div>
    <div class="records k-card" style="padding:0" v-if="records.length">
      <div v-for="r in records" :key="r.id" class="rec">
        <div><div class="rec-type">{{ typeMap[r.record_type]||r.record_type }}</div><div class="rec-time">{{ r.created_at }}</div></div>
        <div class="rec-right">
          <span class="rec-change" :style="{color:Number(r.change_hours)>0?'var(--mint)':'var(--pink)'}">{{ Number(r.change_hours)>0?'+':'' }}{{ r.change_hours }}</span>
          <span class="rec-after">余 {{ r.after_hours }}</span>
        </div>
      </div>
    </div>
    <div v-else class="empty-card k-card"><div class="empty-text">暂无记录</div></div>

    <el-dialog v-model="rechargeVisible" title="充值课时" width="340px">
      <el-form :model="rForm" label-position="top">
        <el-form-item :label="`当前剩余 ${student.remaining_hours} 课时`">
          <el-input-number v-model="rForm.hours" :min="1" :max="999" style="width:100%" />
        </el-form-item>
        <el-form-item label="备注"><el-input v-model="rForm.remark" placeholder="如：续费 20 课时" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rechargeVisible=false">取消</el-button>
        <el-button type="primary" @click="handleRecharge">确认充值</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getStudent, getHourRecords, rechargeStudent } from '@/api/students'

const route = useRoute()
const student = ref<any>(null)
const records = ref<any[]>([])
const rechargeVisible = ref(false)
const rForm = ref({ hours:20, remark:'' })

const statusMap: Record<string,string> = { active:'在读', suspended:'暂停', quit:'退学' }
const typeMap: Record<string,string> = { purchase:'充值', present_deduct:'到课扣课时', makeup_deduct:'补课扣课时', absent_deduct:'缺席扣课时', manual_adjust:'手动调整', refund:'退费' }

const infoItems = computed(() => {
  if (!student.value) return []
  const s = student.value
  return [
    { label:'家长姓名', value: s.parent_name||'-' },
    { label:'联系电话', value: s.phone||'-' },
    { label:'累计购买', value: `${s.total_hours} 课时` },
    { label:'剩余课时', value: `${s.remaining_hours}`, cls: s.remaining_hours<=3?'hours-low':'' },
    { label:'状态', value: statusMap[s.status]||s.status },
  ].filter(Boolean)
})

async function loadData() {
  const id = Number(route.params.id)
  const [sr, rr]: any[] = await Promise.all([getStudent(id), getHourRecords(id)])
  student.value = sr.data; records.value = rr.data
}

async function handleRecharge() {
  await rechargeStudent(student.value.id, rForm.value)
  ElMessage.success('充值成功 ✓'); rechargeVisible.value=false; loadData()
}

onMounted(loadData)
</script>

<style scoped>
.detail { padding-bottom:16px; }

.info-card { padding:4px 16px; }
.ir { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F5F2F8; font-size:14px; }
.ir:last-child { border-bottom:none; }
.ir-label { color:var(--text-secondary); }
.ir-value { font-weight:500; }
.hours-low { color:#D4647A; font-weight:700; }

.records { overflow:hidden; }
.rec { display:flex; justify-content:space-between; align-items:center; padding:10px 16px; border-bottom:1px solid #F5F2F8; }
.rec:last-child { border-bottom:none; }
.rec-type { font-size:14px; font-weight:500; }
.rec-time { font-size:11px; color:var(--text-hint); margin-top:1px; }
.rec-right { text-align:right; }
.rec-change { font-size:15px; font-weight:700; }
.rec-after { font-size:11px; color:var(--text-hint); display:block; margin-top:1px; }

.empty-card { text-align:center; padding:28px; }
.empty-text { color:var(--text-hint); font-size:14px; }
</style>
