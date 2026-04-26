from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from routers import students, class_slots, terms, lessons, dashboard

# 创建所有数据表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Calligraphy Course Manager", version="1.0.0")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(students.router)
app.include_router(class_slots.router)
app.include_router(terms.router)
app.include_router(lessons.router)
app.include_router(dashboard.router)

# 托管前端静态文件
STATIC_DIR = Path(__file__).parent.parent / "frontend" / "dist"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="frontend")
