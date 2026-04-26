<template>
  <div class="app-container">
    <main class="app-main">
      <router-view />
    </main>

    <nav class="tab-bar" v-if="showTabs">
      <router-link to="/" class="tab-item" :class="{ active: currentTab === 'home' }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="3"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="9" y1="4" x2="9" y2="10"/></svg>
        <span>首页</span>
      </router-link>
      <router-link to="/lessons" class="tab-item" :class="{ active: currentTab === 'lessons' }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/></svg>
        <span>课程</span>
      </router-link>
      <router-link to="/manage" class="tab-item" :class="{ active: currentTab === 'manage' }">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        <span>管理</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const currentTab = computed(() => {
  const path = route.path
  if (path === '/') return 'home'
  if (path.startsWith('/lessons')) return 'lessons'
  if (path.startsWith('/manage') || path.startsWith('/students') || path.startsWith('/class-slots') || path.startsWith('/terms')) return 'manage'
  return ''
})

const showTabs = computed(() => {
  const path = route.path
  if (path.includes('/attendance')) return false
  if (path.match(/^\/students\/\d+$/)) return false
  return true
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

:root {
  --bg: #FFF9F5;
  --bg-card: #FFFFFF;
  --bg-pink: #FFF0F3;
  --bg-mint: #EEFBF5;
  --bg-cream: #FFF8ED;
  --bg-lavender: #F3F0FF;

  --pink: #F8A4B8;
  --pink-soft: #FDDCE4;
  --mint: #7ECEC1;
  --mint-soft: #D4F3EB;
  --cream: #F5D98A;
  --cream-soft: #FFF3D1;
  --lavender: #B8A9E8;
  --lavender-soft: #E8E2F8;
  --peach: #F5B895;
  --peach-soft: #FDE8D8;

  --text-primary: #4A3F55;
  --text-secondary: #8E85A0;
  --text-hint: #B8B0C8;

  --radius-s: 10px;
  --radius-m: 14px;
  --radius-l: 20px;
  --radius-xl: 24px;

  --shadow-card: 0 2px 12px rgba(180, 160, 200, 0.08);
  --shadow-btn: 0 2px 8px rgba(180, 160, 200, 0.12);
  --shadow-tab: 0 -2px 16px rgba(180, 160, 200, 0.1);
}

* { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
html, body { height: 100%; }
body { font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text-primary); }
#app { height: 100%; }

.app-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg);
}

.app-main {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 16px;
}

/* Tab bar */
.tab-bar {
  display: flex;
  background: var(--bg-card);
  padding: 6px 16px 10px;
  padding-bottom: calc(10px + env(safe-area-inset-bottom, 0px));
  box-shadow: var(--shadow-tab);
  flex-shrink: 0;
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  text-decoration: none;
  color: var(--text-hint);
  font-size: 11px;
  font-weight: 500;
  padding: 4px 0;
  transition: all 0.25s ease;
  position: relative;
}

.tab-item.active {
  color: var(--pink);
}

.tab-item.active::before {
  content: '';
  position: absolute;
  top: -6px;
  width: 20px;
  height: 3px;
  border-radius: 2px;
  background: var(--pink);
}

/* Global card */
.k-card {
  background: var(--bg-card);
  border-radius: var(--radius-l);
  padding: 16px;
  box-shadow: var(--shadow-card);
}

/* Global soft button */
.k-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  font-family: inherit;
}

.k-btn:active { transform: scale(0.95); }

.k-btn-pink {
  background: linear-gradient(135deg, var(--pink), #F092A8);
  color: #fff;
  box-shadow: 0 3px 12px rgba(248,164,184,0.3);
}
.k-btn-mint {
  background: linear-gradient(135deg, var(--mint), #6CC0B3);
  color: #fff;
  box-shadow: 0 3px 12px rgba(126,206,193,0.3);
}
.k-btn-cream {
  background: linear-gradient(135deg, var(--cream), #E8C56A);
  color: #7A6830;
  box-shadow: 0 3px 12px rgba(245,217,138,0.3);
}
.k-btn-ghost {
  background: var(--bg-pink);
  color: var(--pink);
  box-shadow: none;
}

/* Global transitions */
.k-card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.k-card:active { transform: scale(0.98); }

/* Section label */
.k-section {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 20px 0 10px;
  letter-spacing: 0.5px;
}

/* Page top bar */
.k-top {
  display: flex;
  align-items: center;
  margin-bottom: 14px;
}
.k-top-back {
  background: none;
  border: none;
  color: var(--pink);
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px 4px 0;
  font-family: inherit;
  font-weight: 500;
}
.k-top-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  flex: 1;
}
</style>
