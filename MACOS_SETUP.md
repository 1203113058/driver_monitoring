# macOS 安装指南

本文档提供在 macOS 系统上安装和运行驾驶员监控系统的详细步骤，特别是针对 Apple Silicon (M系列) 芯片优化。

## 环境准备

推荐使用 conda 创建一个 Python 3.10 的虚拟环境：

```bash
# 创建新的Python 3.10环境--如果没有的情况就创建
conda create -n py310 python=3.10 -y
# 激活环境
conda activate py310
```

## 安装依赖

使用专为 macOS 优化的依赖文件安装所需包：

```bash
# 安装依赖
pip install -r requirements_macos.txt
```

如果遇到安装问题，可以尝试单独安装每个包：

```bash
pip install opencv-python==4.11.0.86
pip install mediapipe==0.10.21
pip install numpy==1.26.4
pip install absl-py==2.3.0 attrs protobuf jax jaxlib sentencepiece sounddevice
```

## 运行系统

安装完成后，可以使用以下命令运行面部追踪系统：

```bash
# 使用默认摄像头
python facial.py

# 或指定摄像头ID
python facial.py --webcam 1
```

## 查看可用摄像头

如果需要查看系统中所有可用的摄像头，可以运行：

```bash
python camera_list.py
```

## 疑难解答

如果安装 mediapipe 遇到问题，请确保：

1. 使用的是 Python 3.10 而不是更高版本
2. 尝试重新安装依赖项
3. 确保系统已安装最新的 Xcode 命令行工具

## 退出系统

在运行系统时，按下 Q 键可以退出。 