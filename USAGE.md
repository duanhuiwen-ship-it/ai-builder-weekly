# AI Builder 周报 Skill - 使用说明

## 快速开始

当用户要求生成 AI Builder 周报时:

1. 运行 `python scripts/fetch_content.py` 获取配置
2. 使用 WebSearch 并行抓取各平台内容
3. 尝试获取推文原文（优先），否则使用搜索引擎摘要
4. 将结果填充到 `scripts/output/fetched_data.json`
5. 运行 `python scripts/generate_report.py` 生成报告

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
      "content": "推文内容摘要（无法获取原文时使用）",
      "original_text": "推文完整原文（如果获取到）",
      "has_original_text": true,
      "source": "https://x.com/karpathy/status/xxx",
      "insight": "对产品经理的启示"
    }
  ],
  "podcasts": [...],
  "blogs": [...],
  "top_5": [
    {
      "source": "Karpathy",
      "topic": "LLM Knowledge Bases",
      "summary": "用 LLM 从存储-检索转向生成-编译范式"
    }
  ],
  "trends": [
    {
      "title": "入口迁移加速",
      "description": "多个来源同时指向..."
    }
  ]
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `has_original_text` | 是 | 是否获取到了推文原文 |
| `original_text` | 可选 | 推文完整原文，优先使用 |
| `content` | 是 | 内容摘要（无原文时使用） |
| `insight` | 是 | 对产品经理的启示，具体 actionable |

## 抓取推文原文的策略

1. **WebSearch**: 搜索 `"@handle keyphrase" site:x.com` 格式
2. **第三方站点**: 访问 nitter/fixupx/bestblogs.dev 等镜像站点
3. **博客转载**: 搜索是否有第三方博客引用了完整推文
4. **降级**: 无法获取原文时，使用搜索引擎摘要 + 标注 `has_original_text: false`

## 扩展数据源

编辑 `scripts/sources.json` 添加新的数据源。

## 注意事项

- 确保网络连接正常
- X/Twitter 内容可能需要通过 WebSearch 间接获取
- 报告生成前验证数据完整性
- Top 5 和趋势总结必须基于本周实际内容
