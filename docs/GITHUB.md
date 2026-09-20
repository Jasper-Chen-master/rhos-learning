# GitHub 使用与导入

本项目已发布到私有仓库 [Jasper-Chen-master/rhos-learning](https://github.com/Jasper-Chen-master/rhos-learning)。

## 直接开始

```bash
git clone https://github.com/Jasper-Chen-master/rhos-learning.git
cd rhos-learning
python scripts/study.py today
```

私有仓库需要使用你的 GitHub 账户登录。已有仓库无需再次创建；下面的新建步骤仅用于将来另存副本。

## 方法一：GitHub 网页新建 + 本地 Git 推送

1. 登录 GitHub，点右上角 `+` → `New repository`。
2. 填 `rhos-learning`，选择 Private；不要自动添加 README、.gitignore 或 license。
3. 点 `Create repository`。
4. 解压本项目，在包含 `README.md` 的 `rhos-learning` 文件夹打开终端。
5. 执行下列命令。账户名已按当前连接的 GitHub 填为 `Jasper-Chen-master`；如果换账户需修改地址。

```bash
git init -b main
git add .
git commit -m "Initialize RHOS learning workspace"
git remote add origin https://github.com/Jasper-Chen-master/rhos-learning.git
git push -u origin main
```

若 Git 要求身份，按提示配置自己的 `user.name` 和 `user.email`；登录使用 Git 凭据管理器或 GitHub Desktop 的浏览器授权。
若远程仓库已经有内容，不要强制推送：先 clone 远程仓库，再把本包文件复制进去，检查差异后提交。

## 方法二：GitHub Desktop

在 Desktop 使用 `File → Add Local Repository` 选择解压目录；如果提示不是 Git 仓库，选择在此创建仓库。
提交文件后选择 `Publish repository`，名称填 `rhos-learning`，保留私有选项。不要把整个 zip 当作项目源码上传。

## 每天保存

```bash
python scripts/study.py dashboard
git status
git diff
git add .
git commit -m "Log study progress"
git push
```

## Issues 与可选看板

推送后 `Issues → New issue` 可使用学习任务、卡点、实验、周复盘表单。
如需拖拽看板，可手动创建 GitHub Project，添加 Todo / In progress / Done 状态并将 Issue 加入。
本包提供这些模板，没有替你创建远程 Issues、Project 或关联自动化；文件勾选和 Issue 状态彼此独立。

推荐一个明确任务对应一条 Issue，在描述中链接 `weeks/Wxx.md` 或具体项目。完成后先更新周文件，再关闭 Issue。
公开展示前将自己的独立项目与课程答案分开，并查看课程公布答案的规则。
