(function () {
  const data = window.FS_DATA;
  if (!data) return;

  const STAGE_DRILLS = {
    A0: "D-BR01、D-BR02、D-BR03、D-BP01～D-BP04",
    A1: "D-BP01～D-BP10、D-K11",
    A2: "D-K01～D-K18",
    A3: "D-BP11～D-BP14、D-K06、D-I05、D-I06",
    A4: "D-K07、D-BR01～D-BR15、D-I01～D-I06",
    A5: "D-P01～D-P19、D-R01～D-R12",
    A6: "D-I04～D-I10、D-R09～D-R11、D-E01",
    A7: "D-E01～D-E09",
    A8: "D-E、D-OW；按目标调整，不再追单一标准动作",
  };

  const LAYERS = [
    { id: "L1", title: "先能在水里正常存在", ids: ["A0", "A1"] },
    { id: "L2", title: "建立稳定和基础推进", ids: ["A2", "A3"] },
    { id: "L3", title: "把划水和呼吸真正连接", ids: ["A4", "A5", "A6"] },
    { id: "L4", title: "让技术在真实游泳中持续存在", ids: ["A7", "A8"] },
  ];

  const STAGE_NOTES = {
    A0:
      "不是：脸入水憋住 → 换气时突然吐完 → 慌忙吸气。\n\n" +
      "而是：**脸入水以后持续、自然呼气 → 嘴露出水面以后主要负责快速吸气。** 鼻呼、口呼或口鼻共同均可。关键是不要一直屏住呼吸。不要求每次把肺里空气完全挤空。",
    A1:
      "- 眼睛主要看池底或前下方；颈部自然延伸；不持续抬头看前方。\n" +
      "- 胸部自然进入水中；髋部靠近水面；双腿向后方延伸；拉长但不僵硬。\n" +
      "- 腿沉不一定是腿弱。上游常见：头高、换气抬头、胸不愿入水、塌腰、紧张、手向下压水、前后平衡未建立。不要马上只加打腿力量。",
    A2:
      "主要由髋部带动：大腿带小腿，膝允许自然弯曲，不主动大幅收膝；脚踝放松，脚背延长；双腿上下距离较小、连续；主要上下运动，不是向两侧剪开。向下打与向上回都要有，不能只有单方向用力。\n\n" +
      "作用除推进外：维持身体位置、稳定髋部、平衡划手旋转、支持换气、维持节奏。长距离可减少打腿消耗，但不等于完全停止。",
    A3:
      "- **身体转动：**绕头顶到脚尖长轴左右转。肩髋同向协调，不必机械同角。实际中肩部转动通常可以大于髋部。\n" +
      "- **转肩：**肩带随身体转为前伸、抱水、推水、移臂提供空间。不等于把肩膀耸到耳朵旁。\n" +
      "- **转头：**只在需要换气时明显转向侧面。不换气时：身体在转、肩膀在转，头基本稳定。每次划手头跟着左右摆，会破坏方向、平衡、入水轨迹和换气。",
    A4:
      "向右换气顺序：右臂开始向后划 → 身体右转 → 右肩离水 → 头随身体右转 → 嘴出水快吸 → 头及时回正 → 移臂完成前移入水。\n\n" +
      "不是：手全部划完 → 再抬头 → 找空气。头主要向侧面转，不是向前上方抬。「一只泳镜留在水里」可作为初学提示，不是绝对几何标准。\n\n" +
      "初学建议固定一侧、两划一换。稳定后再补弱侧、左右切换、三划一换等。最终目标不是必须三划一换，而是左右都具备换气能力，并能按需要选择节奏。",
    A5:
      "入水 → 前伸 → 抱水 → 划水 → 推水 → 移臂。\n\n" +
      "- **入水：**同侧肩前；不越过中线；指尖先入水；不拍水。\n" +
      "- **前伸：**来自手臂延伸、肩带向前、身体转动。不必为了更长而过中线、耸肩、在最前方停很久。\n" +
      "- **抱水：**「高肘」更重要的是肘部不要先掉下去，不是肘越高越好。\n" +
      "- **划水：**把水向后推。一直向下压会使上半身暂升、腿易沉、有效推进减少。不必刻意画固定 S 形。\n" +
      "- **推水：**继续到大腿附近。过早在腰旁结束会缩短单次推进、被迫加划频、后程更易疲劳。\n" +
      "- **移臂：**基础适合放松屈肘移臂；直臂移臂也是实际存在的技术，本库保留直臂专项。水下不是一直直臂划。",
    A6:
      "一侧划水 → 身体转动 → 另一侧前伸 → 水上移臂 → 换气按需插入 → 双腿持续稳定。\n\n" +
      "- **极端一：过度追赶。**前手一直等另一只手完全回来 → 停顿、易沉、划频过低。\n" +
      "- **极端二：风车抢手。**一只手刚入水，另一只已急着离开前方 → 前方无稳定延伸、抱水不完整、易下沉。",
    A7:
      "核心不是单纯加米数，而是**距离增加后，动作仍然存在**。观察每 25 米划次、速度、换气急促度、腿位、手臂是否变短、是否抬头。前 25 米好、后 25 米明显变形：优先理解为技术耐力不足或起步太快，不是强行继续加距离。",
    A8:
      "进入这个阶段以后，不再追求单一「标准动作」，而是根据目标调整。\n\n" +
      "- 轻松连续游：呼吸稳定、平衡、放松、较低消耗。\n" +
      "- 长距离：稳定划水、合理划频、技术耐力、配速、左右换气。\n" +
      "- 短距离：更连续打腿、更快划频、更快抱水和移臂、减少换气造成的速度损失。\n" +
      "- 开放水域：抬头观察、左右换气、时机适应、绕标、直线、变速、安全。",
  };

  const $ = (sel, root) => (root || document).querySelector(sel);

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  const DRILL_NAMES = {};
  const DRILL_IDS = {};
  data.drills.forEach(function (d) {
    DRILL_NAMES[d.id] = d.name;
    DRILL_IDS[d.id] = true;
  });

  function drillName(code) {
    if (DRILL_NAMES[code]) return DRILL_NAMES[code];
    const base = code.replace(/[A-Z]$/, "");
    return DRILL_NAMES[base] || "";
  }

  function zhDrillName(code) {
    return drillName(code).replace(/^[A-Za-z][A-Za-z\-]*\s*/, "") || drillName(code);
  }

  function chainStepLabel(raw) {
    const clean = raw.replace(/^→\s*/, "").replace(/。$/, "");
    const m = clean.match(
      /^(D-(?:BP|BR|OW|[KPRIE])\d+[A-Z]?)(\/[A-Z]+)?(?:\s+(.+))?$/
    );
    if (!m) return clean;
    const code = m[1];
    const extra = m[2] || "";
    const rest = m[3] || "";
    if (rest && !/^[A-Za-z][A-Za-z0-9\s\-]*$/.test(rest)) {
      return code + extra + " " + rest;
    }
    const zh = zhDrillName(code);
    if (!zh) return clean;
    return code + extra + " " + zh;
  }

  function withGearLinks(html) {
    return html
      .replace(/正面呼吸管/g, '<a href="../gear/snorkels/">正面呼吸管</a>')
      .replace(/短脚蹼/g, '<a href="../gear/fins/">短脚蹼</a>')
      .replace(/小划手/g, '<a href="../gear/paddles/">小划手</a>');
  }

  function drillHref(code) {
    if (DRILL_IDS[code]) return "#drill-" + code;
    const base = code.replace(/[A-Z]$/, "");
    if (DRILL_IDS[base]) return "#drill-" + base;
    return "#drill-" + code;
  }

  function linkCodes(html) {
    return html.replace(
      /\b(D-(?:BP|BR|OW|[KPRIE])\d+[A-Z]?|C[1-6]-\d{2}|A[0-8])\b/g,
      function (m) {
        const href = m.startsWith("D-")
          ? drillHref(m)
          : m.startsWith("C")
            ? "#sym-" + m
            : "#stage-" + m;
        return '<a href="' + href + '">' + m + "</a>";
      }
    );
  }

  function md(text) {
    const lines = text.replace(/\r/g, "").split("\n");
    let html = "";
    let list = null;
    function closeList() {
      if (list) {
        html += "</" + list + ">";
        list = null;
      }
    }
    function inline(s) {
      s = esc(s);
      s = s.replace(/\[([^\]]+)\]\((#[^)]+)\)/g, '<a href="$2">$1</a>');
      s = s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
      return linkCodes(s);
    }
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (/^\s*$/.test(line)) {
        closeList();
        continue;
      }
      if (/^###\s+/.test(line)) {
        closeList();
        html += "<h4>" + inline(line.replace(/^###\s+/, "")) + "</h4>";
        continue;
      }
      if (/^>\s?/.test(line)) {
        closeList();
        html += '<p class="rule">' + inline(line.replace(/^>\s?/, "")) + "</p>";
        continue;
      }
      const ul = line.match(/^[-*]\s+(.*)$/);
      if (ul) {
        if (list !== "ul") {
          closeList();
          html += "<ul>";
          list = "ul";
        }
        html += "<li>" + inline(ul[1]) + "</li>";
        continue;
      }
      const ol = line.match(/^\d+\.\s+(.*)$/);
      if (ol) {
        if (list !== "ol") {
          closeList();
          html += "<ol>";
          list = "ol";
        }
        html += "<li>" + inline(ol[1]) + "</li>";
        continue;
      }
      closeList();
      html += "<p>" + inline(line) + "</p>";
    }
    closeList();
    return html;
  }

  function renderStages() {
    $("#spine").innerHTML = LAYERS.map(function (layer, li) {
      const bits = layer.ids
        .map(function (id, i) {
          return (
            (i ? '<span class="spine-arr">→</span>' : "") +
            '<a class="spine-n" href="#stage-' +
            id +
            '">' +
            id +
            "</a>"
          );
        })
        .join("");
      return (
        (li ? '<span class="spine-gap" aria-hidden="true"></span>' : "") +
        '<span class="spine-g">' +
        bits +
        "</span>"
      );
    }).join("");

    const byId = {};
    data.stages.forEach(function (s) {
      byId[s.id] = s;
    });

    function stageArticle(s) {
      const note = STAGE_NOTES[s.id] ? md(STAGE_NOTES[s.id]) : "";
      return (
        '<article class="stage" id="stage-' +
        s.id +
        '"><header><span class="id">' +
        s.id +
        '</span><span class="name">' +
        esc(s.name) +
        "</span></header><dl>" +
        "<dt>核心任务</dt><dd>" +
        esc(s.task) +
        "</dd>" +
        "<dt>建议里程碑</dt><dd>" +
        withGearLinks(esc(s.milestone)) +
        "</dd>" +
        "<dt>最常见卡点</dt><dd>" +
        esc(s.stuck) +
        "</dd>" +
        "<dt>优先练习</dt><dd>" +
        linkCodes(esc(STAGE_DRILLS[s.id] || "")) +
        "</dd></dl>" +
        (note ? '<div class="stage-more">' + note + "</div>" : "") +
        "</article>"
      );
    }

    $("#stages").innerHTML = LAYERS.map(function (layer) {
      const range = layer.ids[0] + "–" + layer.ids[layer.ids.length - 1];
      return (
        '<div class="layer-block" id="layer-' +
        layer.id +
        '"><h3 class="layer-lab"><span class="lid">' +
        layer.id +
        "</span>" +
        esc(layer.title) +
        ' <span class="lrange">' +
        range +
        "</span></h3>" +
        layer.ids
          .map(function (id) {
            return stageArticle(byId[id]);
          })
          .join("") +
        "</div>"
      );
    }).join("");
  }

  function renderTests() {
    $("#tests").innerHTML =
      "<table><thead><tr><th>测试结果</th><th>优先怀疑</th></tr></thead><tbody>" +
      data.quickTests
        .map(function (t) {
          return (
            "<tr><td>" +
            withGearLinks(esc(t.result)) +
            "</td><td>" +
            esc(t.suspect) +
            "</td></tr>"
          );
        })
        .join("") +
      "</tbody></table>";
  }

  function renderSymptoms() {
    const order = ["C1", "C2", "C3", "C4", "C5", "C6"];
    let html = "";
    order.forEach(function (g) {
      const items = data.symptoms[g] || [];
      if (!items.length) return;
      const title = items[0].groupTitle;
      html +=
        "<h3 id=\"grp-" +
        g +
        "\">" +
        g +
        " " +
        esc(title) +
        "</h3><table><thead><tr><th>现象</th><th>优先定位</th><th>主要影响</th><th>优先练习</th></tr></thead><tbody>";
      items.forEach(function (s) {
        html +=
          '<tr id="sym-' +
          s.id +
          '"><td><strong>' +
          s.id +
          "</strong> " +
          esc(s.name) +
          "</td><td>" +
          esc(s.locate) +
          "</td><td>" +
          esc(s.impact) +
          "</td><td>" +
          linkCodes(esc(s.drills)) +
          "</td></tr>";
      });
      html += "</tbody></table>";
    });
    $("#symptoms").innerHTML = html;
  }

  function renderDrills() {
    let html = "";
    let last = "";
    data.drills.forEach(function (d) {
      if (d.prefix !== last) {
        if (last) html += "</div>";
        html +=
          '<h3 class="cat-h" id="cat-' +
          d.prefix +
          '">' +
          d.prefix +
          " " +
          esc(d.category) +
          '</h3><div class="drill-grid">';
        last = d.prefix;
      }
      html +=
        '<article class="drill" id="drill-' +
        d.id +
        '"><h3>' +
        d.id +
        " " +
        esc(d.name) +
        (d.en ? ' <span class="en">' + esc(d.en) + "</span>" : "") +
        "</h3>" +
        md(d.body) +
        "</article>";
    });
    if (last) html += "</div>";
    $("#drills").innerHTML = html;
  }

  function renderChains() {
    const rows = data.chains
      .map(function (c) {
        const title = c.title.replace(/^16\.\d+\s+/, "");
        const flow = c.steps
          .map(function (st, i) {
            const clean = chainStepLabel(st);
            return (
              (i ? '<span class="arr" aria-hidden="true">→</span>' : "") +
              "<span>" +
              linkCodes(esc(clean)) +
              "</span>"
            );
          })
          .join("");
        return (
          "<tr><td>" +
          esc(title) +
          '</td><td><div class="order">' +
          flow +
          "</div></td></tr>"
        );
      })
      .join("");
    $("#chains").innerHTML =
      "<table><thead><tr><th>问题</th><th>练习顺序</th></tr></thead><tbody>" +
      rows +
      "</tbody></table>";
  }

  renderStages();
  renderTests();
  renderSymptoms();
  renderDrills();
  renderChains();

  const navLinks = Array.prototype.slice.call(document.querySelectorAll(".side nav a"));
  const sections = navLinks
    .map(function (a) {
      return document.querySelector(a.getAttribute("href"));
    })
    .filter(Boolean);

  const io = new IntersectionObserver(
    function (entries) {
      const vis = entries
        .filter(function (x) {
          return x.isIntersecting;
        })
        .sort(function (a, b) {
          return b.intersectionRatio - a.intersectionRatio;
        })[0];
      if (!vis) return;
      navLinks.forEach(function (a) {
        a.classList.toggle("active", a.getAttribute("href") === "#" + vis.target.id);
      });
    },
    { rootMargin: "-20% 0px -70% 0px", threshold: [0, 0.2, 0.5] }
  );
  sections.forEach(function (s) {
    io.observe(s);
  });
})();
