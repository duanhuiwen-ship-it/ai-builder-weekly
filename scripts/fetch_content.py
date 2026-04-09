#!/usr/bin/env python3
"""
AI Builder 周报 - 内容抓取脚本
从 X/Twitter、播客、博客平台抓取指定时间范围的内容
输出: scripts/output/fetched_data.json
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
SOURCES_FILE = Path(__file__).parent / "sources.json"
OUTPUT_FILE = OUTPUT_DIR / "fetched_data.json"
ERROR_LOG = OUTPUT_DIR / "errors.log"


def load_sources():
    """加载数据源配置"""
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_output_dir():
    """确保输出目录存在"""
    OUTPUT_DIR.mkdir(exist_ok=True)


def log_error(source, error):
    """记录错误日志"""
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {source}: {error}\n")


def format_date_range(start_date, end_date):
    """格式化日期范围"""
    return f"{start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="抓取 AI Builder 动态内容")
    parser.add_argument("--start", type=str, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="结束日期 (YYYY-MM-DD)")
    args = parser.parse_args()
    
    end_date = datetime.strptime(args.end, "%Y-%m-%d") if args.end else datetime.now()
    start_date = datetime.strptime(args.start, "%Y-%m-%d") if args.start else end_date - timedelta(days=7)
    
    sources = load_sources()
    ensure_output_dir()
    
    print(f"📅 抓取时间范围: {format_date_range(start_date, end_date)}")
    print(f"📡 数据源: {len(sources['podcasts'])} 个播客, {len(sources['blogs'])} 个博客, {len(sources['x_accounts'])} 个 X 账号")
    print("-" * 60)
    
    result = {
        "metadata": {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "fetched_at": datetime.now().isoformat()
        },
        "x_twitter": [],
        "podcasts": [],
        "blogs": []
    }
    
    # 输出中间结果供后续处理
    # 实际抓取由 AI 代理通过 WebSearch 完成
    # 此脚本主要负责结构化数据传递
    
    print("\n📋 待抓取列表:")
    print(f"\nX/Twitter 账号 ({len(sources['x_accounts'])}):")
    for acc in sources["x_accounts"]:
        print(f"  - {acc['name']} (@{acc['handle']})")
    
    print(f"\n播客 ({len(sources['podcasts'])}):")
    for pod in sources["podcasts"]:
        print(f"  - {pod['name']}: {pod['url']}")
    
    print(f"\n博客 ({len(sources['blogs'])}):")
    for blog in sources["blogs"]:
        print(f"  - {blog['name']}: {blog['url']}")
    
    # 保存配置到输出文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "config": sources,
            "date_range": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 配置已输出到: {OUTPUT_FILE}")
    print("📝 请使用 AI 代理并行抓取各平台内容")
    
    return sources, start_date, end_date


if __name__ == "__main__":
    main()
