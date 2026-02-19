import folium
import json
import os

with open("prefectures.geojson", encoding="utf-8") as f:
    geo_json = json.load(f)

visited = ["北海道", "東京都", "京都府", "沖縄県"]

info_data = {
    "北海道": {
        "images": ["images/akw1.jpg"],
        "text": "北海道：自然豊かで食べ物が美味しい地域。観光名所や温泉も豊富です。",
        "tags": ["#nature", "#food", "#cold"],
        },
    "沖縄県": {
        "images": ["images/oka.jpg"],
        "text": "沖縄県：美しい海と独自文化。琉球王国の歴史も楽しめます。",
        "tags": ["#sea", "#island", "#culture"],

        },
    }

m = folium.Map(
    location=[37.5, 137],
    zoom_start=5,
    tiles=None,
    control_scale=True,
)

def style_function(feature):
    name = feature["properties"]["name"]
    if name in visited:
        return {"fillColor": "green", "color": "black", "weight": 1, "fillOpacity": 0.7}
    return {"fillColor": "lightgray", "color": "black", "weight": 1, "fillOpacity": 0.3}

def highlight_function(_feature):
    return {"fillColor": "yellow", "color": "orange", "weight": 3, "fillOpacity": 0.9}

def popup_html(pref_name: str) -> str:
    data = info_data.get(pref_name)
    if not data:
        return f"<b>{pref_name}</b><br><span style='color:#666'>(情報なし)</span>"

    images = data.get("images", [])
    text = data.get("text", "")

    img_html = "<div style='color:#666'>(写真なし)</div>"
    if images and os.path.exists(images[0]):
        img_html = f'<img src="{images[0]}" width="180"><br>'

    return f"""
    <div style="width:200px">
        <b>{pref_name}</b><br>
        {img_html}
        <p>{text}</p>
    </div>
    """

def tooltip_html(pref_name: str) -> str:
    data = info_data.get(pref_name)
    if not data:
        return f"<b>{pref_name}</b>"

    images = data.get("images", [])
    img_html = ""
    if images and os.path.exists(images[0]):
        img_html = f'<br><img src="{images[0]}" width="150">'

    return f"<b>{pref_name}</b>{img_html}"

for feature in geo_json["features"]:
    pref_name = feature["properties"]["name"]

    gj = folium.GeoJson(
        feature,
        style_function=style_function,
        highlight_function=highlight_function,
    ).add_to(m)

    # Click popup
    gj.add_child(folium.Popup(popup_html(pref_name), max_width=260))

    # Hover tooltip（写真 + 県名）
    gj.add_child(folium.Tooltip(tooltip_html(pref_name), sticky=True))

    # Dblclick modal（複数写真 + 詳細）
    data = info_data.get(pref_name, {})
    imgs = [p for p in data.get("images", []) if os.path.exists(p)]
    text = data.get("text", "")

    imgs_js = json.dumps(imgs, ensure_ascii=False)
    text_js = json.dumps(text, ensure_ascii=False)
    name_js = json.dumps(pref_name, ensure_ascii=False)

js_code = f"""
<script>
(function() {{
  var layer = {gj.get_name()};
  var prefName = {name_js};

  layer.on('dblclick', function() {{
    openModal(prefName);
  }});
}})();
</script>
"""
gj.add_child(folium.Element(js_code))

   
# ---------- 検索UI ----------
# --- Search UI (append to generated HTML to avoid Jinja issues) ---
search_ui = """
<style>
#searchBox {
  position: fixed;
  top: 10px;
  left: 10px;
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.3);
  z-index: 9999;
  width: 280px;
}
#searchResults {
  margin-top: 8px;
  max-height: 240px;
  overflow-y: auto;
}
.resultItem {
  cursor: pointer;
  padding: 6px;
  border-bottom: 1px solid #eee;
}
.resultItem:hover { background: #f3f3f3; }
</style>

<div id="searchBox">
  <input type="text" id="tagInput" placeholder="#tagで検索" style="width:100%; padding:6px;">
  <div id="searchResults"></div>
</div>
"""

info_json = json.dumps(info_data, ensure_ascii=False)

search_js = f"""
<script>
  var infoData = {info_json};
  function openModal(pref) {
  var data = infoData[pref] || {};
  var imgs = data.images || [];
  var text = data.text || "";

  var old = document.getElementById('modal');
  if (old) old.remove();

  var modal = document.createElement('div');
  modal.id = 'modal';
  modal.style.position = 'fixed';
  modal.style.inset = '0';
  modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
  modal.style.display = 'flex';
  modal.style.justifyContent = 'center';
  modal.style.alignItems = 'center';
  modal.style.zIndex = '10000';

  var content = document.createElement('div');
  content.style.backgroundColor = 'white';
  content.style.padding = '12px';
  content.style.maxWidth = '900px';
  content.style.width = '90%';
  content.style.maxHeight = '85%';
  content.style.overflow = 'auto';
  content.style.borderRadius = '10px';

  var title = document.createElement('h2');
  title.textContent = pref;
  title.style.margin = '0 0 10px 0';
  content.appendChild(title);

  var closeBtn = document.createElement('button');
  closeBtn.textContent = '閉じる';
  closeBtn.onclick = function() { modal.remove(); };
  closeBtn.style.marginBottom = '10px';
  content.appendChild(closeBtn);

  if (imgs.length > 0) {
    var index = 0;
    var imgTag = document.createElement('img');
    imgTag.src = imgs[0];
    imgTag.style.width = '100%';
    imgTag.style.maxHeight = '55vh';
    imgTag.style.objectFit = 'contain';
    imgTag.style.background = '#111';
    imgTag.style.borderRadius = '8px';
    content.appendChild(imgTag);

    if (imgs.length > 1) {
      var nextBtn = document.createElement('button');
      nextBtn.textContent = '次の写真';
      nextBtn.style.marginTop = '8px';
      nextBtn.onclick = function() {
        index = (index + 1) % imgs.length;
        imgTag.src = imgs[index];
      };
      content.appendChild(nextBtn);
    }
  } else {
    var noImg = document.createElement('div');
    noImg.textContent = '(写真なし)';
    noImg.style.color = '#666';
    content.appendChild(noImg);
  }

  var p = document.createElement('p');
  p.textContent = text || '';
  p.style.marginTop = '10px';
  content.appendChild(p);

  modal.addEventListener('click', function(e) {
    if (e.target === modal) modal.remove();
  });

  modal.appendChild(content);
  document.body.appendChild(modal);
}



  function renderResult(pref) {{
    var images = infoData[pref].images || [];
    var tags = infoData[pref].tags || [];
    var imgHtml = "";
    if (images.length > 0) {{
      imgHtml = '<img src="' + images[0] + '" style="width:60px;height:auto;border-radius:6px;">';
    }}

    return (
      '<div style="display:flex;align-items:center;gap:8px;">' +
        imgHtml +
        '<div>' +
          '<div style="font-weight:bold;">' + pref + '</div>' +
          '<div style="font-size:12px;color:#666;">' + tags.join(' ') + '</div>' +
        '</div>' +
      '</div>'
    );
  }}

  document.addEventListener("DOMContentLoaded", function() {{
    var input = document.getElementById("tagInput");
    var resultsDiv = document.getElementById("searchResults");

    input.addEventListener("input", function() {{
      var query = input.value.trim();
      resultsDiv.innerHTML = "";

      if (!query.startsWith("#")) return;

      Object.keys(infoData).forEach(function(pref) {{
        var tags = infoData[pref].tags || [];
        if (tags.indexOf(query) !== -1) {{
          var div = document.createElement("div");
          div.className = "resultItem";

          div.innerHTML = renderResult(pref);

          div.onclick = function() {{
            openModal(pref); // クリックしたら表示
          }};
          resultsDiv.appendChild(div);
        }}
      }});
    }});
  }});
</script>
"""

# まず地図HTMLを保存
m.save("index.html")

# 生成された index.html の </body> の直前に検索UIを差し込む
with open("index.html", "r", encoding="utf-8") as f:
  html = f.read()

insert = search_ui + search_js
html = html.replace("</body>", insert + "\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
  f.write(html)
