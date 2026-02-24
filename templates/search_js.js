console.log("search_js loaded!");

function highlight(text, query) {
  var lower = text.toLowerCase();
  var index = lower.indexOf(query);
  if (index === -1) return text;

  return text.substring(0, index) +
         "<span class='hl'>" +
         text.substring(index, index + query.length) +
         "</span>" +
         text.substring(index + query.length);
}



var infoData = __INFO_JSON__;
window.infoData = infoData;

// =============================
// モーダル表示
// =============================
function openModal(pref) {
  var data = infoData[pref] || {};
  var imgs = data.images || [];
  var text = data.text || "";
  var tags = data.tags || [];

  var old = document.getElementById("modal");
  if (old) old.remove();

  var modal = document.createElement("div");
  modal.id = "modal";
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.right = "0";
  modal.style.bottom = "0";
  modal.style.backgroundColor = "rgba(0,0,0,0.8)";
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
  modal.style.zIndex = "99999";

  var content = document.createElement("div");
  content.style.backgroundColor = "white";
  content.style.padding = "12px";
  content.style.maxWidth = "900px";
  content.style.width = "90%";
  content.style.maxHeight = "85%";
  content.style.overflow = "auto";
  content.style.borderRadius = "10px";

  var title = document.createElement("h2");
  title.textContent = pref;
  title.style.margin = "0 0 10px 0";
  content.appendChild(title);

  if (tags.length > 0) {
    var tagDiv = document.createElement("div");
    tagDiv.textContent = tags.join(" ");
    tagDiv.style.color = "#666";
    tagDiv.style.fontSize = "12px";
    tagDiv.style.margin = "0 0 8px 0";
    content.appendChild(tagDiv);
  }

  var closeBtn = document.createElement("button");
  closeBtn.textContent = "閉じる";
  closeBtn.onclick = function () { modal.remove(); };
  closeBtn.style.marginBottom = "10px";
  content.appendChild(closeBtn);

  if (imgs.length > 0) {
    var index = 0;
    var imgTag = document.createElement("img");
    imgTag.src = imgs[0];
    imgTag.style.width = "100%";
    imgTag.style.maxHeight = "55vh";
    imgTag.style.objectFit = "contain";
    imgTag.style.background = "#111";
    imgTag.style.borderRadius = "8px";
    content.appendChild(imgTag);

    if (imgs.length > 1) {
      var nextBtn = document.createElement("button");
      nextBtn.textContent = "次の写真";
      nextBtn.style.marginTop = "8px";
      nextBtn.onclick = function () {
        index = (index + 1) % imgs.length;
        imgTag.src = imgs[index];
      };
      content.appendChild(nextBtn);
    }
  } else {
    var noImg = document.createElement("div");
    noImg.textContent = "(写真なし)";
    noImg.style.color = "#666";
    content.appendChild(noImg);
  }

  var p = document.createElement("p");
  p.textContent = text || "";
  p.style.marginTop = "10px";
  content.appendChild(p);

  modal.addEventListener("click", function (e) {
    if (e.target === modal) modal.remove();
  });

  modal.appendChild(content);
  document.body.appendChild(modal);
}

// =============================
// ホバー表示用HTML
// =============================
function tooltipHtml(pref) {
  var data = infoData[pref] || {};
  var imgs = data.images || [];
  var text = data.text || "";

  var imgHtml = "";
  if (imgs.length > 0) {
    imgHtml =
      '<img src="' + imgs[0] +
      '" style="width:160px;height:auto;border-radius:6px;display:block;margin-bottom:6px;">';
  } else {
    imgHtml = '<div style="color:#666">(写真なし)</div>';
  }

  return (
    '<div style="width:180px;">' +
      '<div style="font-weight:bold;margin-bottom:4px;">' + pref + "</div>" +
      imgHtml +
      '<div style="font-size:12px;color:#444;line-height:1.2;">' + text + "</div>" +
    "</div>"
  );
}

// =============================
// 検索結果1件のHTML
// =============================
function renderResult(pref, query) {
  var images = (infoData[pref] && infoData[pref].images) || [];
  var tags = (infoData[pref] && infoData[pref].tags) || [];
  var imgHtml = "";

  if (images.length > 0) {
    imgHtml = '<img src="' + images[0] + '" style="width:60px;height:auto;border-radius:6px;">';
  }

  // 🔥 ここで matchedTags をちゃんと作る
  var matchedTags = tags
    .filter(function(t) {
      var clean = t.replace(/^#/, "").toLowerCase();
      return clean.includes(query);
    })
    .map(function(t) {
      var clean = t.replace(/^#/, "");
      return "#" + highlight(clean, query);
    })
    .join(" ");

  return (
    '<div style="display:flex;align-items:center;gap:8px;">' +
      imgHtml +
      '<div>' +
        '<div style="font-weight:bold;">' + pref + '</div>' +
        '<div style="font-size:12px;color:#666;">' + matchedTags + '</div>' +
      '</div>' +
    '</div>'
  );
}

document.addEventListener("DOMContentLoaded", function () {

  // ===== 自前ホバープレビュー=====
  function ensureHoverBox() {
    var box = document.getElementById("hoverPreview");
    if (box) return box;

    box = document.createElement("div");
    box.id = "hoverPreview";
    box.style.position = "fixed";
    box.style.pointerEvents = "none";
    box.style.zIndex = "99999";
    box.style.display = "none";
    box.style.background = "white";
    box.style.border = "1px solid #000";
    box.style.borderRadius = "8px";
    box.style.padding = "8px";
    box.style.boxShadow = "0 6px 18px rgba(0,0,0,0.25)";
    box.style.maxWidth = "220px";
    document.body.appendChild(box);
    return box;
  }

  var hoverBox = ensureHoverBox();

  function showHoverBox(html, x, y) {
    hoverBox.innerHTML = html;
    hoverBox.style.display = "block";
    hoverBox.style.left = (x + 14) + "px";
    hoverBox.style.top  = (y + 14) + "px";
  }

  function hideHoverBox() {
    hoverBox.style.display = "none";
  }

  // ===== geo_json_* を全部集めて hover を付ける =====
  var layers = [];
  for (var k in window) {
    if (k.startsWith("geo_json_") && window[k] && typeof window[k].eachLayer === "function") {
      layers.push(window[k]);
    }
  }
  console.log("geo_json layers:", layers.length);

  layers.forEach(function (geoLayer) {
    geoLayer.eachLayer(function (layer) {
      var pref = layer.feature && layer.feature.properties && layer.feature.properties.name;
      if (!pref) return;

      layer.on("mouseover", function (e) {
        var ev = e.originalEvent;
        if (!ev) return;
        showHoverBox(tooltipHtml(pref), ev.clientX, ev.clientY);
      });

      layer.on("mousemove", function (e) {
        var ev = e.originalEvent;
        if (!ev) return;
        showHoverBox(tooltipHtml(pref), ev.clientX, ev.clientY);
      });

      layer.on("mouseout", function () {
        hideHoverBox();
      });

      layer.on("click", function () {
        openModal(pref);
      });
    });
  });

  // ===== #タグ検索 =====
  var input = document.getElementById("tagInput");
  var resultsDiv = document.getElementById("searchResults");
  if (!input || !resultsDiv) {
    console.log("search UI not found");
    return;
  }
input.addEventListener("input", function () {
  var raw = (input.value || "").trim();
  resultsDiv.innerHTML = "";
  if (!raw) return;

  var query = raw.replace(/^#/, "").toLowerCase().trim();

  Object.keys(infoData || {}).forEach(function (pref) {
    var tags = (infoData[pref] && infoData[pref].tags) || [];

    var hit = false;

    // 🔥 #から始まり、3文字以上
    if (raw.startsWith("#") && query.length >= 3) {
      hit = tags.some(function(t) {
        var tag = String(t).toLowerCase().replace(/^#/, "");
        return tag.includes(query);
      });
    }

    if (hit) {
      var div = document.createElement("div");
      div.className = "resultItem";
      div.innerHTML = renderResult(pref, query);
      div.onclick = function () { openModal(pref); };
      resultsDiv.appendChild(div);
    }
  });
});

});