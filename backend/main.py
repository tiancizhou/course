from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import students, class_slots, terms, lessons, dashboard

# 创建所有数据表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="书法课时管理系统", version="1.0.0")

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


@app.get("/")
def root():
    return {"message": "书法课时管理系统 API", "version": "1.0.0"}
