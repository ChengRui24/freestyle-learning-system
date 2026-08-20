# 自由泳完整学习体系 3.0

静态页：学习阶段、现象诊断、专项练习库。无构建步骤。

## 本地

用浏览器打开 `index.html`，或：

```bash
python3 -m http.server 8080
```

左侧导航跳转到各章节。

## GitHub Pages

已发布：<https://chengrui24.github.io/freestyle-learning-system/>

源分支为 `main`，站点根目录为仓库根。含 `.nojekyll`。

## 更新内容

改 `source.md` 后执行：

```bash
python3 tools/extract.py
```

会重写 `data.json` 与 `data.js`。
