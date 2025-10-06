# vLLM Docker 项目

基于 vLLM 的高性能大语言模型推理服务 Docker 部署方案。

## 项目概述

本项目提供了一个完整的 vLLM Docker 部署环境，支持：

- **高性能推理**: 基于 PagedAttention 和 Continuous Batching 技术
- **Docker 容器化**: 简化部署和环境管理
- **模型管理**: 支持从 ModelScope 下载和管理模型
- **OpenAI 兼容**: 提供标准 OpenAI API 接口

## 快速开始

### 1. 下载模型

使用项目提供的脚本下载模型：

```bash
# 下载默认模型
python download_model.py

# 下载指定模型
python download_model.py qwen/Qwen3-0.6B

# 仅校验模型完整性
python download_model.py --verify qwen/Qwen3-0.6B
```

### 2. 启动服务

使用 Docker Compose 启动 vLLM 服务：

```bash
docker-compose up -d
```

### 3. 验证服务

```bash
# 健康检查
curl http://localhost:8786/health

# 查看可用模型
curl http://localhost:8786/v1/models
```

## 项目结构

```
vllm-docker/
├── docker-compose.yml      # Docker Compose 配置
├── download_model.py       # 模型下载脚本
├── models/                 # 模型存储目录
└── README.md              # 项目文档
```

## 配置说明

### Docker Compose 配置

当前配置针对 Qwen3-4B-Instruct-2507-AWQ 模型优化：

- **端口映射**: 8786:8000
- **GPU 支持**: 自动检测所有可用 GPU
- **内存优化**: 90% GPU 内存利用率，10GB 交换空间
- **API 认证**: 内置 API 密钥保护

### 模型参数

```yaml
command: >
  --model /models/Eslzzyl/Qwen3-4B-Instruct-2507-AWQ
  --served-model-name Qwen3-4B-Instruct-2507-AWQ
  --api-key liangmj@123
  --max-model-len 32768
  --max-num-seqs 1
  --swap-space 10
  --gpu-memory-utilization 0.9
  --enable-auto-tool-choice
  --tool-call-parser hermes
  --trust-remote-code
  --disable-log-requests
```

## API 使用

### OpenAI 兼容接口

```bash
# 聊天完成
curl -X POST "http://localhost:8786/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer liangmj@123" \
  -d '{
    "model": "Qwen3-4B-Instruct-2507-AWQ",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
  }'
```

## 高级配置

### 自定义模型

1. 下载新模型到 `models/` 目录
2. 修改 `docker-compose.yml` 中的模型路径
3. 重启服务

### 性能调优

- **GPU 内存**: 根据显存大小调整 `gpu-memory-utilization`
- **并发限制**: 通过 `max-num-seqs` 控制并发请求数
- **序列长度**: `max-model-len` 决定最大 token 长度

## 故障排查

### 常见问题

1. **GPU 内存不足**
   - 减少 `gpu-memory-utilization` 值
   - 使用更小的模型或量化版本

2. **模型加载失败**
   - 检查模型文件完整性
   - 验证模型路径是否正确

3. **API 调用失败**
   - 确认 API 密钥正确
   - 检查网络连接和端口映射

### 日志查看

```bash
# 查看服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f Qwen3-4B-Instruct-2507-AWQ
```

## 技术支持

- **vLLM 官方文档**: https://docs.vllm.ai/
- **Docker 官方文档**: https://docs.docker.com/
- **ModelScope 模型库**: https://modelscope.cn/