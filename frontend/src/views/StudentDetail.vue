<template>
  <div>
    <el-card shadow="hover" style="margin-bottom: 20px">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <div style="font-size: 18px; font-weight: bold">学生详情</div>
        <el-button @click="$router.back()">返回</el-button>
      </div>
      <el-descriptions :column="3" border v-if="student">
        <el-descriptions-item label="姓名">{{ student.name }}</el-descriptions-item>
        <el-descriptions-item label="家长姓名">{{ student.parent_name }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ student.phone }}</el-descriptions-item>
        <el-descriptions-item label="累计购买课时">{{ student.total_hours }}</el-descriptions-item>
        <el-descriptions-item label="剩余课时">
          <span :style="{ color: student.remaining_hours <= 3 ? '#f56c6c' : '#67c23a', fontWeight: 'bold' }">
            {{ student.remaining_hours }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">{{ statusMap[student.status] }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="3">{{ student.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card shadow="hover">
      <div style="font-size: 16px; font-weight: bold; margin-bottom: 12px">课时流水</div>
      <el-table :data="records" stripe>
        <el-table-column prop="created_at" label="时间" width="180" />
        <el-table-column label="变化" width="100">
          <template #default="{ row }">
            <span :style="{ color: Number(row.change_hours) > 0 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
              {{ Number(row.change_hours) > 0 ? '+' : '' }}{{ row.change_hours }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="before_hours" label="变化前" width="100" />
        <el-table-column prop="after_hours" label="变化后" width="100" />
        <el-table-column label="类型" width="140">
          <template #default="{ row }">{{ recordTypeMap[row.record_type] || row.record_type }}</template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getStudent, getHourRecords } from '@/api/students'

const route = useRoute()
const student = ref<any>(null)
const records = ref<any[]>([])

const statusMap: Record<string, string> = { active: '在读', suspended: '暂停', quit: '退学' }
const recordTypeMap: Record<string, string> = {
  purchase: '充值',
  present_deduct: '到课扣课时',
  makeup_deduct: '补课扣课时',
  absent_deduct: '缺席扣课时',
  manual_adjust: '手动调整',
  refund: '退费',
}

async function loadData() {
  const id = Number(route.params.id)
  const [studentRes, recordsRes]: any[] = await Promise.all([getStudent(id), getHourRecords(id)])
  student.value = studentRes.data
  records.value = recordsRes.data
}

onMounted(loadData)
</script>
