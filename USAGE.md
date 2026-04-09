# AI Builder 周报 Skill - 使用说明

## 快速开始

当用户要求生成 AI Builder 周报时:

1. 运行 `python scripts/fetch_content.py` 获取配置
2. 使用 WebSearch 并行抓取各平台内容
3. 将结果填充到 `scripts/output/fetched_data.json`
4. 运行 `python scripts/generate_report.py` 生成报告

## 数据格式

`fetched_data.json` 结构:

```json
{
  "metadata": {
    "start_date": "2026-04-02",
    "end_date": "2026-04-09",
    "fetched_at": "2026-04-09T10:00:00"
  },
  "x_twitter": [
    {
      "name": "Andrej Karpathy (@karpathy)",
      "content": "推文内容摘要",
      "source": "https://x.com/karpathy/status/xxx",
      "insight": "对产品经理的启示"
    }
  ],
  "podcasts": [...],
  "blogs": [...]
}
```

## 扩展数据源

编辑 `scripts/sources.json` 添加新的数据源。

## 注意事项

- 确保网络连接正常
- X/Twitter 内容可能需要通过 WebSearch 间接获取
- 报告生成前验证数据完整性
