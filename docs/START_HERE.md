# 第一次使用

1. 从 [GitHub 仓库](https://github.com/Jasper-Chen-master/rhos-learning) clone 到电脑，或下载 ZIP 后解压。
2. 打开本地 `rhos-learning` 文件夹；命令操作见 [GitHub 使用指南](GITHUB.md)。
3. 打开 [W01](../weeks/W01.md)，先做第一天任务。
4. 在此文件夹打开终端，运行 `python scripts/study.py today`。
5. 打开命令打印的日志文件；记录目标、实际用时、代码路径和明天第一步。
6. 完成一项后在周文件中把 `[ ]` 改为 `[x]`；运行 `python scripts/study.py dashboard`。
7. 周日填写对应的 `reviews/Wxx.md`，用证据判断是否进入下周。

## 常用命令

```bash
# 按本机当天日期创建日志；计划在 2026-09-21 开始
python scripts/study.py today

# 指定日期补记，未来日期只创建空白模板，不算打卡完成
python scripts/study.py today --date 2026-09-21

# 定位第 1 周复盘，不覆盖已有内容
python scripts/study.py review 1

# 重新统计时长、必做完成率、验收进度
python scripts/study.py dashboard

# 检查仓库结构与本地 Markdown 链接
python scripts/study.py check
```

日志开头的 `minutes: 0` 改成实际学习分钟数，完成记录后将 `completed: false` 改成 `completed: true`。
时长独立于完成状态汇总；未完成但实际学过的分钟也会计入。完成状态用于统计打卡天数。
命令使用本机日期；时区不对时传 `--date`。计划外日期仍可记录，但不会硬分配到某一周。

## 只使用 GitHub 网页也可以

进入周文件点击编辑，把 `[ ]` 改成 `[x]` 后提交。按 [每日模板](../templates/daily.md) 在 `logs/` 建立 `YYYY-MM-DD.md`。
`DASHBOARD.md` 是生成的快照；网页改完任务后，需本地运行 dashboard 再 push 才会更新。
Issue 适合讨论卡点，周 Markdown 是任务完成率的唯一来源；两者不会自动同步。

## 时间不够时

先保留本周必做与验收，选做顺延。延期写在复盘里即可；日期是参考，不是硬截止。
开始日期若整体改变，手动同步 `plan.json` 和周文件日期；现有命令不提供自动重排。
