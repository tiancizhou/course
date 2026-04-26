<template>
  <el-container style="height: 100vh">
    <el-aside width="200px" style="background-color: #304156">
      <div style="padding: 20px 0; text-align: center; color: #fff; font-size: 16px; font-weight: bold">
        书法课时管理
      </div>
      <el-menu
        :default-active="currentPath"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/">
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/students">
          <span>学生管理</span>
        </el-menu-item>
        <el-menu-item index="/class-slots">
          <span>固定时间段</span>
        </el-menu-item>
        <el-menu-item index="/terms">
          <span>学期管理</span>
        </el-menu-item>
        <el-menu-item index="/lessons">
          <span>课程管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main style="background-color: #f0f2f5; padding: 20px; overflow-y: auto">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentPath = computed(() => {
  // /students/123 -> /students
  const path = route.path
  if (path.startsWith('/students')) return '/students'
  return path
})
</script>
