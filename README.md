# 人生结算单 · 随机十条

从《高性价比人生指南》（[eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter)）的正文里随机抽 10 条人生建议的网页。每条带书的成本标签（钱 / 时间 / 毅力）、收益量级与口径、证据等级 A/B/C，点开可以看原文数据、备注与文献来源。

- 在线页面：GitHub Pages（仓库启用后访问根地址）
- `index.html`：单文件页面，数据（772 条）已内联，双击即可用，不依赖后端
- `build_page.py`：从 `items.json` 重新生成页面的脚本
- `items.json`：从原书 34 节正文解析出的结构化条目，字段包括节号、条号、成本标签、说人话、收益、证据等级、来源、备注

## 数据与授权

正文与条目版权归原作者，按 CC BY 4.0 授权；代码部分 MIT。本页只做抽取与呈现，成本/收益档位是作者判断，不替代医生、律师、会计。

## 重新生成

```bash
python3 build_page.py   # 输出 人生结算单-随机十条.html
```

生成后把它复制或重命名为 `index.html` 即可作为 Pages 首页。
