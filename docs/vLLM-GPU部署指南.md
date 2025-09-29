# vLLM GPU部署指南

## 核心理解

vLLM的本质是一个专为大语言模型推理优化的高性能服务框架，通过以下关键技术实现高效GPU加速：

- **PagedAttention**: 内存分页机制，最大化GPU显存利用率
- **Continuous Batching**: 连续批处理，提高GPU计算效率
- **Tensor Parallelism**: 张量并行，支持多GPU分布式推理

## 安装方法

### 基础安装

```bash
# GPU安装（推荐）
pip install vllm

# CPU安装（功能受限）
pip install vllm-cpu
```

### 特定CUDA版本

```bash
# 指定CUDA版本（如11.8或12.6）
export CUDA_VERSION=118
pip install vllm-cuda${CUDA_VERSION}

# 或使用uv安装器
uv pip install vllm --torch-backend=auto
```

### AMD GPU支持（ROCm）

```bash
# 安装PyTorch ROCm版本
pip uninstall torch -y
pip install --no-cache-dir --pre torch --index-url https://download.pytorch.org/whl/nightly/rocm6.3

# 安装flash-attention ROCm版本
git clone https://github.com/ROCm/flash-attention.git
cd flash-attention
git checkout b7d29fb
GPU_ARCHS="gfx90a" python3 setup.py install
```

## Docker部署

### NVIDIA GPU

```bash
# 使用官方镜像
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model Qwen/Qwen3-0.6B
```

### AMD GPU（ROCm）

```bash
# 运行ROCm容器
docker run -it \
    --network=host \
    --device /dev/kfd \
    --device /dev/dri \
    --ipc=host \
    rocm/vllm:rocm6.2_mi300_ubuntu20.04_py3.9_vllm_0.6.4
```

## Kubernetes部署

### NVIDIA GPU配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-gpu
spec:
  template:
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        resources:
          limits:
            cpu: "10"
            memory: 20G
            nvidia.com/gpu: "1"
        volumeMounts:
        - name: shm
          mountPath: /dev/shm
      volumes:
      - name: shm
        emptyDir:
          medium: Memory
          sizeLimit: "2Gi"
```

### AMD GPU配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-amd
spec:
  template:
    spec:
      hostNetwork: true
      hostIPC: true
      containers:
      - name: vllm
        image: rocm/vllm:rocm6.2_mi300_ubuntu20.04_py3.9_vllm_0.6.4
        resources:
          limits:
            cpu: "10"
            memory: 20G
            amd.com/gpu: "1"
```

## 关键配置要点

### 共享内存配置
vLLM需要足够的共享内存用于张量并行推理：
- Docker: `--ipc=host` 或 `--shm-size=2G`
- Kubernetes: 挂载`/dev/shm`卷

### 环境变量
```bash
# CUDA相关
export CUDA_HOME=/usr/local/cuda
export PATH="${CUDA_HOME}/bin:$PATH"

# HuggingFace认证
export HUGGING_FACE_HUB_TOKEN=your_token
```

### GPU优化参数
```bash
# 启用分块预填充
vllm serve --enable-chunked-prefill --max_num_batched_tokens 1024

# 张量并行（多GPU）
vllm serve --tensor-parallel-size 2
```

## 验证部署

启动服务后验证：

```bash
# 健康检查
curl http://localhost:8000/health

# OpenAI兼容API测试
curl http://localhost:8000/v1/models
```

## 故障排查

1. **GPU检测失败**: 检查驱动版本和CUDA安装
2. **内存不足**: 增加共享内存或减少batch size
3. **模型加载失败**: 验证HuggingFace token和模型路径

## 性能调优建议

- 使用最新CUDA/ROCm驱动
- 根据GPU型号调整`tensor-parallel-size`
- 监控GPU利用率和内存使用
- 考虑使用量化模型减少显存占用