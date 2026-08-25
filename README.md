# 成人游泳训练

静态站点：自由泳学习体系，以及 FINIS 呼吸管、划手掌、脚蹼选型。无构建步骤。

## 本地

```bash
python3 -m http.server 8080
```

打开 <http://127.0.0.1:8080/>。

- `/` 主页
- `/learn/` 自由泳完整学习体系 3.0
- `/gear/snorkels/` 呼吸管
- `/gear/paddles/` 划手掌
- `/gear/fins/` 脚蹼

## GitHub Pages

已发布：<https://chengrui24.github.io/freestyle-learning-system/>

源分支为 `main`，站点根目录为仓库根。含 `.nojekyll`。旧的学习页锚点（如 `#use`）会从主页转到 `/learn/`。

## 更新学习体系内容

改 `learn/source.md` 后执行：

```bash
python3 tools/extract.py
```

会重写 `learn/data.json` 与 `learn/data.js`。
