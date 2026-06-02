# OpenAI 翻译插件

基于 OpenAI API 的翻译插件，支持 DeepSeek、GPT 等模型。

## 配置

在 `cnf/const.py` 中配置：

```python
# 翻译工具选择 OpenAI
translate_tool = "OpenAI"

# OpenAI API 配置
translate_openai_key = "your-api-key"
translate_openai_model = "deepseek/deepseek-v4-flash"
translate_openai_base_url = "http://serv.newapi.cn:8022/v1"
```

## 配置说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `translate_tool` | 翻译工具选择，设为 `OpenAI` | `"OpenAI"` |
| `translate_openai_key` | API Key | `"sk-xxxxx"` |
| `translate_openai_model` | 模型名称 | `"deepseek/deepseek-v4-flash"` 或 `"gpt-4o-mini"` |
| `translate_openai_base_url` | API 地址 | `"http://serv.newapi.cn:8022/v1"` |

## 支持的模型

- DeepSeek 系列：`deepseek/deepseek-v4-flash`、`deepseek/deepseek-chat`
- OpenAI 系列：`gpt-4o`、`gpt-4-turbo`、`gpt-3.5-turbo`
- 其他兼容 OpenAI API 格式的模型

## 使用方法

1. 安装依赖：
```bash
pip install openai
```

2. 配置 `cnf/const.py` 中的 API Key 和模型

3. 运行程序：
```bash
python main.py
```

## 工作原理

插件通过调用 OpenAI ChatGPT API，将 Nessus 漏洞的英文名称、描述和解决方案翻译成中文：

- **输入**：漏洞英文信息（name_en, describe_en, solution_en）
- **输出**：翻译后的中文信息（name_cn, describe_cn, solution_cn）
- **翻译结果**：自动保存到本地 `vuln.db` 数据库，下次无需重复翻译

## 注意事项

1. API 调用受 QPS 限制约束，默认 `translate_qps = 9`
2. 翻译结果默认自动写入本地数据库 (`translate_auto_db = True`)
3. 如需更换翻译引擎，只需修改 `translate_tool` 和对应的配置