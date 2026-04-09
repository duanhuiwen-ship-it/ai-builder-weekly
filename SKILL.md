---
name: ai-builder-weekly-report
description: 抓取关注的 AI Builder 在 X/Twitter、播客、博客平台的最新动态，整理成面向产品经理的周报。当用户需要生成 AI 行业动态周报、AI Builder 动态汇总、产品经理周报、或提及"ai builder 周报"、"ai 动态周报"时使用此 skill。
---

# AI Builder 周报生成

自动抓取多个平台的 AI Builder 动态，生成面向产品经理的结构化周报。

## 快速开始

1. 确认需要抓取的数据源（使用默认配置或修改 `scripts/sources.json`）
2. 运行抓取脚本: `python scripts/fetch_content.py`
3. 运行报告生成脚本: `python scripts/generate_report.py`
4. 报告输出到当前目录: `AI_Builder_Weekly_Report_YYYY-MM-DD.md`

## 工作流程

```
Task Progress:
- [ ] 步骤 1: 确认时间范围（默认近 7 天）
- [ ] 步骤 2: 抓取 X/Twitter 账号动态
- [ ] 步骤 3: 抓取播客最新内容
- [ ] 步骤 4: 抓取博客最新文章
- [ ] 步骤 5: 整合数据生成周报
- [ ] 步骤 6: 验证报告完整性
```

### 步骤 1: 确认时间范围

默认抓取近 7 天的内容。如需自定义:

```bash
python scripts/fetch_content.py --start 2026-04-01 --end 2026-04-08
```

### 步骤 2-4: 抓取内容

使用并行子代理同时抓取不同平台:

- **X/Twitter**: 使用 WebSearch 搜索各账号近期推文
- **播客**: 搜索各播客频道的最新节目
- **博客**: 访问博客页面获取最新文章

抓取脚本会输出 JSON 格式的中间结果到 `scripts/output/fetched_data.json`，便于调试。

### 步骤 5: 生成周报

运行报告生成脚本:

```bash
python scripts/generate_report.py
```

报告结构:
```
# AI Builder 周报 | YYYY-MM-DD - YYYY-MM-DD

## 本周核心洞察总结
（6 个关键趋势，每个包含标题和 2-3 句摘要）

## X/Twitter 动态
### 姓名
**输出内容**: xxx
**source**: xxx
**产品经理洞察**: xxx

## 播客动态
（同上格式）

## 博客动态
（同上格式）
```

### 步骤 6: 验证

检查生成的报告:
- 每个平台至少有 2 条有效内容
- 所有 source 链接可访问
- 产品经理洞察具有 actionable 的建议

## 数据源配置

数据源定义在 `scripts/sources.json`:

```json
{
  "podcasts": [
    {
      "name": "Latent Space",
      "url": "https://www.youtube.com/@LatentSpacePod"
    }
  ],
  "blogs": [
    {
      "name": "Anthropic Engineering",
      "url": "https://www.anthropic.com/engineering"
    }
  ],
  "x_accounts": [
    { "name": "Andrej Karpathy", "handle": "karpathy" }
  ]
}
```

## 输出格式规范

每条动态使用以下格式:

```markdown
### 姓名 (@handle)
**输出内容**: [1-3 句摘要，包含核心观点]
**source**: [链接]
**产品经理洞察**: [2-4 句对产品经理的启示，具体 actionable]
```

## 周报质量标准

1. **覆盖度**: 至少覆盖 3 个平台，每个平台 2+ 条内容
2. **时效性**: 仅包含指定时间范围内的内容
3. **洞察力**: 产品经理洞察必须具体、可操作，避免泛泛而谈
4. **准确性**: source 链接必须可访问且与内容匹配
5. **语言**: 使用中文，保持专业但易读的语气

## 常见问题

**Q: 某些账号/平台没有新内容怎么办？**
A: 跳过该条目，仅报告有实际更新的来源。

**Q: 如何调整周报的语气和深度？**
A: 修改 `scripts/generate_report.py` 中的 prompt 模板。

**Q: 抓取失败如何处理？**
A: 脚本会输出错误日志到 `scripts/output/errors.log`，检查后重试失败的源。
