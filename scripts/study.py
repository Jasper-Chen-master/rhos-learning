#!/usr/bin/env python3
"""Zero-dependency Markdown study tracker. Run from any working directory."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def plan(root):
    return json.loads((root / 'plan.json').read_text(encoding='utf-8'))


def for_date(root, day):
    return next((w for w in plan(root)['weeks']
                 if date.fromisoformat(w['start']) <= day <= date.fromisoformat(w['end'])), None)


def create_daily(root, day):
    path = root / 'logs' / f'{day}.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    week = for_date(root, day)
    content = (root / 'templates/daily.md').read_text(encoding='utf-8')
    content = content.replace('YYYY-MM-DD', str(day)).replace('# 每日学习记录', f'# {day} 每日学习记录')
    if week:
        number = week['week']
        content += f'\n对应计划：[W{number:02d} · {week["title"]}](../{week["path"]})\n'
    else:
        content += '\n此日期在原 13 周计划之外，可以正常记录学习。\n'
    try:
        with path.open('x', encoding='utf-8') as file:
            file.write(content)
    except FileExistsError:
        return path, False
    return path, True


def count_section(text, marker):
    match = re.search(rf'<!-- {marker}:start -->(.*?)<!-- {marker}:end -->', text, re.S)
    if not match:
        raise ValueError(f'缺少 {marker} 统计区块')
    boxes = re.findall(r'^- \[([ xX])\] ', match[1], re.M)
    return sum(x.lower() == 'x' for x in boxes), len(boxes)


def read_logs(root):
    logs = []
    for path in sorted((root / 'logs').glob('????-??-??.md')):
        day = date.fromisoformat(path.stem)
        text = path.read_text(encoding='utf-8')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
        if not match:
            raise ValueError(f'{path.name}: 缺少日志头部')
        fields = {}
        for line in match[1].splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                if key.strip() in fields:
                    raise ValueError(f'{path.name}: 重复字段 {key.strip()}')
                fields[key.strip()] = value.strip()
        if fields.get('date') != str(day):
            raise ValueError(f'{path.name}: date 与文件名不一致')
        raw = fields.get('minutes', '')
        if not re.fullmatch(r'\d+', raw) or not 0 <= int(raw) <= 1440:
            raise ValueError(f'{path.name}: minutes 必须是 0 到 1440 的整数')
        if fields.get('completed') not in ('true', 'false'):
            raise ValueError(f'{path.name}: completed 必须为 true 或 false')
        logs.append({'day': day, 'minutes': int(raw), 'completed': fields['completed'] == 'true'})
    return logs


def dashboard(root):
    logs = read_logs(root)
    today = date.today()
    # Future planning entries never inflate actual study totals.
    actual = [x for x in logs if x['day'] <= today]
    future = len(logs) - len(actual)
    rows = []; core_done = core_total = check_done = check_total = 0
    for w in plan(root)['weeks']:
        text = (root / w['path']).read_text(encoding='utf-8')
        done, total = count_section(text, 'core')
        passed, checks = count_section(text, 'checks')
        core_done += done; core_total += total
        check_done += passed; check_total += checks
        matches = [x for x in actual if w['start'] <= str(x['day']) <= w['end']]
        minutes = sum(x['minutes'] for x in matches)
        days = sum(x['completed'] for x in matches)
        state = '已验收' if done == total and passed == checks and total and checks else (
            '待验收' if done == total and total else '进行中' if done or passed or minutes or days else '未开始')
        rows.append(f'| [W{w["week"]:02d}]({w["path"]}) | {w["title"]} | {done}/{total} | {passed}/{checks} | {minutes / 60:.1f} h | {days} | {state} |')
    total_minutes = sum(x['minutes'] for x in actual)
    days = sum(x['completed'] for x in actual)
    outside = sum(x['minutes'] for x in actual if for_date(root, x['day']) is None)
    pct = core_done / core_total * 100 if core_total else 0
    content = f'''# 学习进度面板

更新于 {today}（本机日期）。由 `python scripts/study.py dashboard` 生成；不要手动编辑本文件。

**必做任务：{core_done}/{core_total}（{pct:.0f}%） · 验收项：{check_done}/{check_total} · 实际学习：{total_minutes / 60:.1f} h · 完成打卡：{days} 天**

| 周次 | 主题 | 必做 | 验收 | 时长 | 打卡天数 | 状态 |
|---|---|---|---|---|---|---|
''' + '\n'.join(rows) + f'''

统计规则：只计周文件指定区块的勾选；选做和项目 TODO 不重复计数。验收项全部通过且必做完成才标记“已验收”。
时长读取日志 `minutes`；打卡读取 `completed: true`；没有记录的天不自动补 2 小时。
周时长按计划中的日历日期归属；跨周补课请在日志注明实际学习周。每周缓冲可用于休息，预算与顺延规则见总路线。
计划外学习时长：{outside / 60:.1f} h（包含在总时长，不属于某一周）。未来日期日志 {future} 份，不计实际时长与打卡。
Issue、Project 看板与 Markdown 不自动同步；周复盘结论由你人工填写。

[总路线](ROADMAP.md) · [每日记录](logs/README.md) · [项目](projects/README.md)
'''
    path = root / 'DASHBOARD.md'
    path.write_text(content, encoding='utf-8')
    return path


def check(root):
    errors = []
    config = plan(root)
    weeks = config['weeks']
    if [w['week'] for w in weeks] != list(range(1, 14)):
        errors.append('plan.json 必须包含有序的 W01–W13')
    for week in weeks:
        try:
            if date.fromisoformat(week['end']) < date.fromisoformat(week['start']):
                raise ValueError('结束日期早于开始日期')
            text = (root / week['path']).read_text(encoding='utf-8')
            for marker in ('core', 'checks'):
                if count_section(text, marker)[1] == 0:
                    errors.append(f'{week["path"]}: {marker} 没有任务')
        except (ValueError, OSError) as exc:
            errors.append(f'W{week["week"]}: {exc}')
    for path in root.rglob('*.md'):
        if any(part.startswith('.') for part in path.relative_to(root).parts):
            continue
        text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = target.split('#')[0]
            if target and not (path.parent / target).exists():
                errors.append(f'{path.relative_to(root)}: 链接不存在 {target}')
    try:
        read_logs(root)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description='每日打卡、周复盘入口与学习进度统计')
    sub = parser.add_subparsers(dest='command', required=True)
    daily = sub.add_parser('today', help='创建或定位日志，不覆盖已有笔记')
    daily.add_argument('--date', type=date.fromisoformat, default=date.today(), metavar='YYYY-MM-DD')
    review = sub.add_parser('review', help='定位某一周的复盘文件')
    review.add_argument('week', type=int, choices=range(1, 14), metavar='1..13')
    sub.add_parser('dashboard', help='根据实际记录更新进度面板')
    sub.add_parser('check', help='检查结构、任务统计区块与本地 Markdown 链接')
    args = parser.parse_args()
    try:
        if args.command == 'today':
            path, created = create_daily(ROOT, args.date)
            print(('已创建：' if created else '已存在，未覆盖：') + str(path))
        elif args.command == 'review':
            path = ROOT / 'reviews' / f'W{args.week:02d}.md'
            if not path.exists():
                raise ValueError(f'复盘模板不存在：{path}')
            print(path)
        elif args.command == 'dashboard':
            print('已更新：' + str(dashboard(ROOT)))
        else:
            errors = check(ROOT)
            if errors:
                print('\n'.join(errors), file=sys.stderr)
                return 1
            print('检查通过：13 周结构、统计区块、日志格式与本地 Markdown 链接。')
    except (OSError, ValueError, KeyError) as exc:
        print(f'错误：{exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
