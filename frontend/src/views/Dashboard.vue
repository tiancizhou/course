<template>
  <div>
    <!-- 顶部统计卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div style="font-size: 14px; color: #909399">活跃学生</div>
          <div style="font-size: 28px; font-weight: bold; margin-top: 8px">{{ dashboard.total_students }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div style="font-size: 14px; color: #909399">今日待上课</div>
          <div style="font-size: 28px; font-weight: bold; margin-top: 8px; color: #409eff">{{ dashboard.today_pending_count }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div style="font-size: 14px; color: #909399">待续课学生</div>
          <div style="font-size: 28px; font-weight: bold; margin-top: 8px; color: #e6a23c">{{ dashboard.low_hour_students.length }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div style="font-size: 14px; color: #909399">欠课时学生</div>
          <div style="font-size: 28px; font-weight: bold; margin-top: 8px; color: #f56c6c">{{ dashboard.zero_hour_students.length }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷操作 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="24">
        <el-card shadow="hover">
          <div style="font-size: 16px; font-weight: bold; margin-bottom: 12px">快捷操作</div>
          <el-button type="primary" @click="$router.push('/students')">新增学生</el-button>
          <el-button type="success" @click="$router.push('/class-slots')">管理时间段</el-button>
          <el-button type="warning" @click="$router.push('/terms')">创建学期</el-button>
          <el-button type="info" @click="$router.push('/lessons')">查看课程</el-button>
        </el-card>
      </el-col>
    </el-row>

    <!-- 待续课 & 欠课时提醒 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="12">
        <el-card shadow="hover" v-if="dashboard.low_hour_students.length > 0">
          <div style="font-size: 16px; font-weight: bold; color: #e6a23c; margin-bottom: 12px">待续课学生（剩余课时 ≤ 3）</div>
          <el-table :data="dashboard.low_hour_students" size="small">
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="remaining_hours" label="剩余课时" width="100" />
            <el-table-column prop="phone" label="电话" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" v-if="dashboard.zero_hour_students.length > 0">
          <div style="font-size: 16px; font-weight: bold; color: #f56c6c; margin-bottom: 12px">欠课时学生（剩余课时 ≤ 0）</div>
          <el-table :data="dashboard.zero_hour_students" size="small">
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="remaining_hours" label="剩余课时" width="100" />
            <el-table-column prop="phone" label="电话" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 今日课程 -->
    <el-card shadow="hover" style="margin-bottom: 20px">
      <div style="font-size: 16px; font-weight: bold; margin-bottom: 12px">今日课程</div>
      <el-empty v-if="dashboard.today_lessons.length === 0" description="今天没有课程" />
      <el-table v-else :data="dashboard.today_lessons" size="small">
        <el-table-column prop="slot_name" label="班级" width="150" />
        <el-table-column label="时间" width="120">
          <template #default="{ row }">{{ row.start_time }} - {{ row.end_time }}</template>
        </el-table-column>
        <el-table-column prop="student_count" label="学生数" width="80" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : row.status === 'cancelled' ? 'info' : 'warning'" size="small">
              {{ statusMap[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/lessons/${row.id}/attendance`)">
              {{ row.status === 'completed' ? '查看' : '点名' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 本周课程 -->
    <el-card shadow="hover">
      <div style="font-size: 16px; font-weight: bold; margin-bottom: 12px">本周课程</div>
      <el-empty v-if="dashboard.week_lessons.length === 0" description="本周没有课程" />
      <el-table v-else :data="dashboard.week_lessons" size="small">
        <el-table-column label="日期" width="120">
          <template #default="{ row }">{{ row.lesson_date }} {{ weekdayNames[row.weekday] }}</template>
        </el-table-column>
        <el-table-column prop="slot_name" label="班级" width="150" />
        <el-table-column label="时间" width="120">
          <template #default="{ row }">{{ row.start_time }} - {{ row.end_time }}</template>
        </el-table-column>
        <el-table-column prop="student_count" label="学生数" width="80" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : row.status === 'cancelled' ? 'info' : 'warning'" size="small">
              {{ statusMap[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/lessons/${row.id}/attendance`)">
              {{ row.status === 'completed' ? '查看' : '点名' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDashboard } from '@/api/dashboard'

const weekdayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const statusMap: Record<string, string> = { scheduled: '待上课', completed: '已完成', cancelled: '已取消' }

const dashboard = ref<any>({
  total_students: 0,
  today_lessons: [],
  week_lessons: [],
  low_hour_students: [],
  zero_hour_students: [],
  today_pending_count: 0,
})

async function loadData() {
  const res: any = await getDashboard()
  dashboard.value = res.data
}

onMounted(loadData)
</script>
