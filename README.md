# 自由泳完整学习体系 3.0

静态页：学习阶段、现象诊断、专项练习库。无构建步骤。

## 本地

用浏览器打开 `index.html`，或：

```bash
python3 -m http.server 8080
```

左侧导航跳转到各章节。

## GitHub Pages

1. 把本仓库推到 GitHub。
2. Settings → Pages → Source 选 `main` / root。
3. 站点入口为根目录 `index.html`。

仓库已含 `.nojekyll`，避免 Jekyll 忽略下划线路径。

## 更新内容

改 `source.md` 后执行：

```bash
python3 tools/extract.py
```

会重写 `data.json` 与 `data.js`。
