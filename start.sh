#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "========================================"
echo "  书法课时管理系统 - 启动脚本"
echo "========================================"
echo

# 拉取最新代码
echo "[1/5] 拉取最新代码..."
git pull || echo "[警告] git pull 失败，继续使用本地代码"
echo

# 后端：安装依赖
echo "[2/5] 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
echo

# 前端：安装依赖并构建
echo "[3/5] 安装前端依赖..."
cd ../frontend
npm install
echo

echo "[4/5] 构建前端..."
npm run build
echo

# 启动后端
echo "[5/5] 启动后端服务..."
cd ../backend
echo
echo "========================================"
echo "  服务已启动"
echo "  后端地址: http://localhost:6000"
echo "  API文档:  http://localhost:6000/docs"
echo "========================================"
echo
uvicorn main:app --host 0.0.0.0 --port 6000
