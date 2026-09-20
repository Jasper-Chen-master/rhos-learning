# 开发环境

学习管理脚本只依赖 Python 3.10+ 标准库，不需要 GPU，也不需要安装深度学习包。

前期练习可使用下面的独立环境：

```bash
conda create -n rhos-learning python=3.11
conda activate rhos-learning
pip install numpy matplotlib pillow jupyter
jupyter notebook
```

Windows 下学习 Linux 命令时使用 WSL/Linux 终端；日常 Python 日志命令可直接在 PowerShell 运行。
到 W6 再依据硬件和 [PyTorch 官方安装入口](https://pytorch.org/get-started/locally/) 选择命令，不在此硬编码 CUDA 版本。
CS231n 作业按对应年份的官方环境说明配置；官方 Colab 环境与本地环境可能不同，单独记录。

每个实验记录 Python/框架版本、设备、数据版本、随机种子和复现命令。项目依赖放各自目录，不把不同复现工程挤进一个环境。
