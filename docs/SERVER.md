# 服务器练习清单

把下列占位符换成已获准使用的账户/服务器；共享 GPU 遵守课题组调度方式。

```bash
ssh USER@HOST
conda activate YOUR_ENV
nvidia-smi
tmux new -s train
CUDA_VISIBLE_DEVICES=2 python train.py
```

只在确实有且可用的 GPU 2 时用这个编号；进程内这张卡通常映射为 `cuda:0`。
tmux 中按 `Ctrl+b` 后按 `d` 暂离，之后运行 `tmux attach -t train` 返回。
关闭 SSH 不等于关闭 tmux 会话；服务器重启、进程崩溃或资源被回收仍会停止训练。

- [ ] 能连接并找到自己的工作目录。
- [ ] 能在 tmux 内运行任务，断开终端后重新连接。
- [ ] 能查看 GPU / 使用课题组规定的调度方式。
- [ ] checkpoint 同时保存模型、优化器和训练步数，按项目需要保存随机数/调度器状态。
- [ ] 能从 checkpoint 恢复，核对日志与训练步数。

没有服务器时：先在本地 Linux/WSL 用长时间命令练习 tmux；用 CPU 完成保存/恢复逻辑。
远程连接与真实 GPU 操作保持“未验收”，不把替代练习当作已经完成服务器训练。
