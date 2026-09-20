# RHOS Learning · 从基础代码到小型复现

一个以代码和实验为中心的 13 周学习工作区。每周 10 小时学习、2 小时验收、2 小时缓冲或休息；先做核心，再考虑选做。

进入关键阶段前使用 [数学与独立验收](docs/READINESS.md)，W09–W10 提前验证最终选题。

**从这里开始：[使用指南](docs/START_HERE.md) → [W01 任务](weeks/W01.md)**

| 我想做什么 | 入口 |
|---|---|
| 看 13 周整体安排 | [ROADMAP](ROADMAP.md) |
| 看完成率、验收和学习时长 | [进度面板](DASHBOARD.md) |
| 每天记录学习与卡点 | [每日打卡](logs/README.md) |
| 做周末能力复盘 | [复盘索引](reviews/README.md) |
| 管理练习项目与最终报告 | [项目索引](projects/README.md) |
| 记录与比较实验 | [实验模板](templates/experiment.md) |
| 追踪 CS231n 全部题目 | [作业清单](practice/cs231n/README.md) |
| 查学习资料 | [资料入口](docs/RESOURCES.md) |
| 使用 GitHub / 配置环境 | [GitHub 指南](docs/GITHUB.md) · [环境](docs/SETUP.md) |

## 日常使用

在仓库根目录执行（只需 Python 3.10+；Windows 的 `python` 不可用时改成 `py`）：

```bash
python scripts/study.py today
python scripts/study.py dashboard
```

第一条创建当天打卡，重复执行不会覆盖；第二条读取实际勾选和日志，更新进度面板。
结束学习时填写日志，把完成的周任务从 `[ ]` 改成 `[x]`，再提交 Git。

## 结构

- `weeks/`：13 周必做清单、每日安排、验收、选做。
- `logs/`：按需生成每日日志，记录实际分钟数。
- `reviews/`：13 周复盘，记录“能做”和“只看懂”的差距。
- `projects/`：基础练习、最终小实验与报告；后两个目录可共用代码和数据，不要求四个独立项目。
- `practice/`：Python、小练习与 CS231n 作业工作区。
- `notes/`：概念笔记、排错与待解决问题。
- `templates/`：每日记录、实验、概念与论文阅读模板。
- `scripts/`：零第三方依赖的学习管理命令。
- `.github/`：Issue 表单、PR 模板、结构检查工作流。

这是仓库架构与任务模板，模型训练代码和实验结果由学习过程中逐步完成；未填内容不代表已有成果。
