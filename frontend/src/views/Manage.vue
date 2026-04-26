<template>
  <div class="manage">
    <div class="manage-header">
      <div class="mh-title">管理</div>
      <div class="mh-sub">学生 · 时间段 · 学期</div>
    </div>

    <div class="manage-grid">
      <div class="mg-item k-card" @click="$router.push('/students')" style="--c: var(--pink-soft); --ic: var(--pink);">
        <div class="mg-icon">👤</div>
        <span>学生管理</span>
      </div>
      <div class="mg-item k-card" @click="$router.push('/class-slots')" style="--c: var(--mint-soft); --ic: var(--mint);">
        <div class="mg-icon">🕐</div>
        <span>时间段</span>
      </div>
      <div class="mg-item k-card" @click="$router.push('/terms')" style="--c: var(--lavender-soft); --ic: var(--lavender);">
        <div class="mg-icon">📅</div>
        <span>学期管理</span>
      </div>
    </div>

    <div class="manage-grid" style="margin-top:14px">
      <div class="mg-item k-card" @click="$router.push('/students')" style="--c: var(--cream-soft); --ic: var(--cream);">
        <div class="mg-icon">✨</div>
        <span>新增学生</span>
      </div>
      <div class="mg-item k-card" @click="$router.push('/terms')" style="--c: var(--peach-soft); --ic: var(--peach);">
        <div class="mg-icon">📋</div>
        <span>生成课程</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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
  border: none;
}

.mg-item:active { transform: scale(0.95); }

.mg-icon { font-size: 26px; margin-bottom: 6px; }
.mg-item span { font-size: 12px; font-weight: 600; color: var(--text-primary); }
</style>
