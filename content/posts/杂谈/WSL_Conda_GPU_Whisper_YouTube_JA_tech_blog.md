---
title: "WSL + Conda + GPU Whisper：从 YouTube 日语音声到台本/字幕的一站式流水线（含踩坑大全）"
date: 2026-02-05
draft: False 
---

# WSL + Conda + GPU Whisper：从 YouTube 日语音声到台本/字幕的一站式流水线（含踩坑大全）
起因：听着音声，突然想起自己半途而废的日语学习，遂有此。

> 目标：输入一个 YouTube URL，自动下载视频/音频，用 Whisper 转录成日语台本（txt）与字幕（srt/vtt），并把所有产物放进以“视频标题”命名的文件夹中。  
> 环境：WSL2（Ubuntu）+ conda + NVIDIA GPU（以 RTX 4060 8GB 为例）

---

## 1. 总览：流水线与目录结构

**流水线：**

1) YouTube URL  
2) `yt-dlp` 下载视频（或仅音频）  
3) `ffmpeg` 抽取 / 规整音频（16kHz、单声道 wav）  
4) `whisper`（openai-whisper CLI）转录  
5) 输出：`txt`（台本）、`srt/vtt`（字幕）、`json`（结构化段落信息）

**推荐目录结构（按视频标题建文件夹）：**

```
<视频标题>/
  meta.json               # 可选：yt-dlp 元信息（含标题、时长、频道等）
  video.mp4               # 下载视频
  audio_16k_mono.wav      # Whisper 最稳输入
  audio_16k_mono.txt      # 台本
  audio_16k_mono.srt      # 字幕（时间轴）
  audio_16k_mono.vtt
  audio_16k_mono.json
```

---

## 2. 环境选择：为什么推荐 Python 3.10（conda）

**结论：Python 3.10 是 Whisper 工具链最省心的版本。**

理由（工程视角）：

- `openai-whisper`、`yt-dlp`、`ffmpeg` 组合在 3.10 上兼容性最好
- GPU 相关的 `torch` wheel / conda 包覆盖最稳
- 3.11/3.12 更容易遇到二进制依赖的“版本锁”或源码编译回退

**创建环境：**
```bash
conda create -n whisper python=3.10 -y
conda activate whisper
python -m pip install -U pip
```

---

## 3. GPU 基础检查：确认 WSL 真的能用 GPU

### 3.1 WSL 内确认 GPU 直通
```bash
nvidia-smi
```
能看到 GPU 型号/驱动版本即为 OK。

### 3.2 Python 侧确认 CUDA 可用（torch）
```bash
python -c "import torch; print(torch.__version__); print('cuda:', torch.cuda.is_available()); print('device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
```

---

## 4. PyTorch 关键坑 ①：ImportError `iJIT_NotifyEvent`（MKL/Intel OpenMP 版本冲突）

### 4.1 症状
运行 `import torch` 报：
```
ImportError: ... libtorch_cpu.so: undefined symbol: iJIT_NotifyEvent
```

### 4.2 根因（常见）
conda 环境中 **MKL / intel-openmp 过新（例如 2025.x）**，导致 `libtorch_cpu.so` 动态链接时符号不匹配。

### 4.3 修复策略（推荐）
把 MKL / intel-openmp pin 到兼容版本（例如 2024.0 系列），并补齐 ITT 运行库：

```bash
conda install -y "mkl=2024.*"
```

> 工程建议：**“不要追新 MKL”，优先追能稳定提供 wheel 的组合**。音声学习这种高频工具链，稳定性价值远大于“最新”。

---

## 5. PyTorch 关键坑 ②：`torch.cuda.is_available()==False`（即使 nvidia-smi 正常）

### 解决办法
不太推荐用conda安装torch等，用pip显示指定GPU版本会好很多

---

## 6. ffmpeg 关键坑：apt 找不到 `ffmpeg`（Ubuntu 未启用 universe）

### 6.1 症状
```
E: Unable to locate package ffmpeg
```
或提示 snap。

### 6.2 根因
WSL/Ubuntu 精简安装常常未启用 `universe` 软件源，而 `ffmpeg` 位于 `universe`。

### 6.3 修复（推荐用 apt，不推荐 snap）
```bash
sudo add-apt-repository universe
sudo apt update
sudo apt install -y ffmpeg
ffmpeg -version
```

---

## 7. 代理关键坑：Windows “全局代理”不等于 WSL 终端走代理

### 7.1 症状
- 浏览器能访问 YouTube
- WSL 中 `yt-dlp` 仍然无法下载

### 7.2 根因
WSL 中的 Linux 进程不会自动继承 Windows 代理设置。`yt-dlp` 只会用：

- `--proxy` 参数
- 或环境变量 `http_proxy / https_proxy / all_proxy`
- 或 cookies / 登录等机制

### 7.3 最常见误区：用 `/etc/resolv.conf` 的 `nameserver` 当“Windows 主机 IP”
`/etc/resolv.conf` 的 `nameserver` 是 **DNS 转发器地址**，不等于 Windows 主机网关地址，拿它当代理地址常导致：
```
Connection refused
```

### 7.4 正确做法：从路由表拿 Windows 网关 IP
```bash
WIN_IP=$(ip route | awk '/default/ {print $3}')
echo $WIN_IP
```

### 7.5 端口探测（非常有效）
假设你的代理 HTTP 端口是 7890，SOCKS5 是 7891：
```bash
sudo apt install -y netcat-openbsd
nc -vz $WIN_IP 7890
nc -vz $WIN_IP 7891
```
- succeeded/open：端口可达  
- refused：代理没开“允许局域网连接/Allow LAN”或只绑定在 127.0.0.1

### 7.6 让 yt-dlp 走代理
```bash
yt-dlp --proxy "http://$WIN_IP:7890" "<URL>"
# 或
yt-dlp --proxy "socks5://$WIN_IP:7891" "<URL>"
```

### 7.7 永久设置（可选）
```bash
export http_proxy="http://$WIN_IP:7890"
export https_proxy="http://$WIN_IP:7890"
export all_proxy="socks5://$WIN_IP:7891"
```

---

## 8. yt-dlp 下载策略：视频/音频、合并格式与常用命令

### 8.1 下载最兼容的 mp4（视频+音频合并）
```bash
yt-dlp   -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"   --merge-output-format mp4   "<YouTube_URL>"
```

参数解读：
- `bv*`：最佳视频流（prefer mp4）
- `ba`：最佳音频流（prefer m4a）
- `+`：合并
- `/`：回退策略（找不到就选单文件 mp4）

### 8.2 只下载音频（为转录而生）
```bash
yt-dlp -f ba -x --audio-format m4a "<YouTube_URL>"
```

### 8.3 受限视频（登录/年龄限制）常用手段
从浏览器导入 cookies：
```bash
yt-dlp --cookies-from-browser chrome "<YouTube_URL>"
```

---

## 9. 音频预处理：统一成 16k 单声道 wav（Whisper 最稳输入）

即便 Whisper 能直接吃 mp4/m4a，也建议统一预处理，提高稳定性并减少玄学问题：

```bash
ffmpeg -i "video.mp4" -ac 1 -ar 16000 -vn "audio_16k_mono.wav"
```

---

## 10. Whisper 使用方法：模型选择、输出格式与 GPU/CPU

### 10.1 安装（CLI）
```bash
pip install -U openai-whisper
```

### 10.2 核心命令（建议输出 all：txt+srt+vtt+json）
```bash
whisper "audio_16k_mono.wav"   --language ja   --task transcribe   --model medium   --device cuda   --output_format all   --output_dir out
```

### 10.3 模型选择建议（以 8GB 显存为例）
- 日常稳态：`medium`
- 快速预览：`small`
- `large` 不推荐（显存压力、速度压力明显）

> 实测经验：`medium` 在 RTX 4060 8GB 上显存占用约 ~5GB 属于正常范围，说明 FP16 推理链路通常是对的。

### 10.4 GPU 不可用时先用 CPU 跑通流程（务实策略）
```bash
whisper "audio_16k_mono.wav" --language ja --task transcribe --model small --device cpu --output_format srt --output_dir out
```

---

## 11. 一键自动化：Python 脚本实现（URL -> 文件夹 -> 全部产物）

推荐把流程固化成脚本，输入 URL 自动：

- 用 `yt-dlp -J` 取视频标题
- 创建以标题命名的文件夹
- 下载 `video.mp4`
- `ffmpeg` 抽 `audio_16k_mono.wav`
- `whisper` 输出台本/字幕到同一目录

> 实践建议：脚本中把代理作为参数 `--proxy`，并对标题做文件名清洗（Windows/Unix 都安全）。

---

## 12. 排障速查清单（按概率从高到低）

### 下载失败（yt-dlp）
- `pip install -U yt-dlp`（优先）
- 代理未传入 WSL（见第 7 节）
- 需要 cookies（见 8.3）

### ffmpeg 不存在
- 启用 universe 并安装（见第 6 节）

### torch import 报 iJIT_NotifyEvent
- 降级 MKL/Intel OpenMP（见第 4 节）

### nvidia-smi 正常但 torch.cuda False
- 添加 `/usr/lib/wsl/lib` 到 ldconfig（见第 5 节）
- 排查 `LD_LIBRARY_PATH` 劫持（见第 5.4 节）

---

## 参考链接
```text
https://github.com/yt-dlp/yt-dlp
https://github.com/openai/whisper
https://pytorch.org/get-started/locally/
https://ffmpeg.org/
```
