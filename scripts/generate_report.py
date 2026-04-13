#!/usr/bin/env python3
"""
AI Builder 周报 - 报告生成脚本
将抓取的数据整理成面向产品经理的 Markdown 周报
输入: scripts/output/fetched_data.json (包含抓取结果)
输出: AI_Builder_Weekly_Report_YYYY-MM-DD.md
"""

import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"


def load_fetched_data():
    """加载抓取数据"""
    data_file = OUTPUT_DIR / "fetched_data.json"
    if not data_file.exists():
        print(f"❌ 未找到抓取数据文件: {data_file}")
        print("请先运行 fetch_content.py 并确保数据已填充")
        sys.exit(1)
    
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_report(data, output_path=None):
    """生成 Markdown 周报"""
    
    metadata = data.get("metadata", {})
    start_date = metadata.get("start_date", "未知")
    end_date = metadata.get("end_date", "未知")
    
    x_entries = data.get("x_twitter", [])
    podcast_entries = data.get("podcasts", [])
    blog_entries = data.get("blogs", [])
    
    # 构建数据说明
    has_original_x = [e.get("has_original_text", False) for e in x_entries]
    original_count = sum(1 for x in has_original_x if x)
    summary_count = len(x_entries) - original_count
    
    data_note = f"**数据说明**: 本周报中 X/Twitter 部分，{original_count} 个账号获取到了推文原文"
    if summary_count > 0:
        data_note += f"，{summary_count} 个账号因 X 平台反爬限制，仅能通过搜索引擎摘要获取动态方向"
    data_note += "。"
    
    lines = []
    
    # 标题
    lines.append(f"# AI Builder 周报 | {start_date} - {end_date}")
    lines.append("")
    lines.append(f"> {data_note}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 本周速览
    lines.append("## 本周速览")
    lines.append("")
    
    # Top 5 表格
    lines.append("### Top 5 值得关注的内容")
    lines.append("")
    lines.append("| 排名 | 来源 | 核心内容 | 一句话摘要 |")
    lines.append("|------|------|----------|------------|")
    
    # Top 5 需要从数据中提取（这里提供结构，实际内容由 AI 填充）
    top_5 = data.get("top_5", [])
    for i, item in enumerate(top_5, 1):
        lines.append(f"| {i} | {item.get('source', '')} | {item.get('topic', '')} | {item.get('summary', '')} |")
    
    if not top_5:
        lines.append("| 1 | - | - | *由 AI 根据本周内容填充* |")
        lines.append("| 2 | - | - | - |")
        lines.append("| 3 | - | - | - |")
        lines.append("| 4 | - | - | - |")
        lines.append("| 5 | - | - | - |")
    
    lines.append("")
    
    # 整体趋势
    lines.append("### 整体 AI 发展趋势")
    lines.append("")
    
    trends = data.get("trends", [])
    if trends:
        for trend in trends:
            lines.append(f"**{trend.get('title', '')}**: {trend.get('description', '')}")
            lines.append("")
    else:
        lines.append("*(本部分由 AI 根据本周多个来源的共同指向自动生成 5 个趋势方向)*")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # X/Twitter 动态
    lines.append("## X/Twitter 动态")
    lines.append("")
    
    for entry in x_entries:
        name = entry.get('name', '未知')
        source = entry.get('source', '')
        insight = entry.get('insight', '')
        has_original = entry.get('has_original_text', False)
        
        lines.append(f"### {name}")
        
        if has_original:
            lines.append(f"**推文原文**: {entry.get('original_text', entry.get('content', ''))}")
        else:
            lines.append(f"**输出内容**: {entry.get('content', '')}")
        
        lines.append(f"**source**: {source}")
        lines.append(f"**产品经理洞察**: {insight}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # 播客动态
    lines.append("## 播客动态")
    lines.append("")
    
    for entry in podcast_entries:
        lines.append(f"### {entry.get('name', '未知')}")
        lines.append(f"**输出内容**: {entry.get('content', '')}")
        lines.append(f"**source**: {entry.get('source', '')}")
        lines.append(f"**产品经理洞察**: {entry.get('insight', '')}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # 博客动态
    lines.append("## 博客动态")
    lines.append("")
    
    for entry in blog_entries:
        lines.append(f"### {entry.get('name', '未知')}")
        lines.append(f"**输出内容**: {entry.get('content', '')}")
        lines.append(f"**source**: {entry.get('source', '')}")
        lines.append(f"**产品经理洞察**: {entry.get('insight', '')}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # 页脚
    lines.append("---")
    lines.append("")
    lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append(f"*数据来源: X/Twitter、YouTube Podcasts、技术博客*")
    lines.append("")
    
    report_content = "\n".join(lines)
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"✅ 报告已生成: {output_path}")
    else:
        print(report_content)
    
    return report_content


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="生成 AI Builder 周报")
    parser.add_argument("-o", "--output", type=str, help="输出文件路径")
    args = parser.parse_args()
    
    data = load_fetched_data()
    
    output_path = args.output or f"AI_Builder_Weekly_Report_{datetime.now().strftime('%Y-%m-%d')}.md"
    
    generate_report(data, output_path)
    
    # 打印统计信息
    x_count = len(data.get("x_twitter", []))
    podcast_count = len(data.get("podcasts", []))
    blog_count = len(data.get("blogs", []))
    original_count = sum(1 for e in data.get("x_twitter", []) if e.get("has_original_text", False))
    
    print(f"\n📊 统计:")
    print(f"  X/Twitter: {x_count} 条 (原文: {original_count}, 摘要: {x_count - original_count})")
    print(f"  播客: {podcast_count} 条")
    print(f"  博客: {blog_count} 条")
    print(f"  总计: {x_count + podcast_count + blog_count} 条")


if __name__ == "__main__":
    main()
