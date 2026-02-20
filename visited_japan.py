import folium
import json
import os

with open("prefectures.geojson", encoding="utf-8") as f:
    geo_json = json.load(f)

visited = ["北海道", "東京都", "京都府", "沖縄県","神奈川県","長野県","福岡県","熊本県",
           "山口県","静岡県","大分県","広島県","鳥取県","栃木県","大阪府","兵庫県","奈良県",
           ]

info_data = {
    "北海道": {
        "images": ["images/hokkaido/akw1.jpg"],
        "text": "北海道：自然豊かで食べ物が美味しい地域。観光名所や温泉も豊富です。",
        "tags": ["#nature", "#food", "#cold"],
        },
    "沖縄県": {
        "images": ["images/okinawa/oka.jpg"],
        "text": "沖縄県：美しい海と独自文化。琉球王国の歴史も楽しめます。",
        "tags": ["#sea", "#island", "#culture",],
        },
    
    "東京都": {
        "images": ["images/tokyo/tokyo01.jpg"],
        "text": "東京都：都会。",
        "tags": ["#city", "#skytree", "#capital","nightview",],
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
    return {"fillColor": "yellow", "color": "black", "weight": 1, "fillOpacity": 0.9}

def popup_html(pref_name: str) -> str:
    data = info_data.get(pref_name)
    if not data:
        return f"<b>{pref_name}</b><br><span style='color:#666'>(情報なし)</span>"

    images = data.get("images", [])
    text = data.get("text", "")

    img_html = ""
    for img in images:
        if os.path.exists(img):
            img_html += f'<img src="{img}" width="180" style="margin-bottom:8px;"><br>'

    if not img_html:
     img_html = "<div style='color:#666'>(写真なし)</div>"

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
        control=False,
    ).add_to(m)

    

    # Hover tooltip（写真 + 県名）
   
    gj.add_child(folium.Tooltip(tooltip_html(pref_name), sticky=False))

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

  layer.on('click', function() {{
    openModal(prefName);
  }});
}})();
</script>
"""
    gj.add_child(folium.Element(js_code))

    
  # ---------- 検索UI & JS 読み込み ----------

# UI読み込み
with open("templates/search_ui.html", encoding="utf-8") as f:
    search_ui = f.read()

# JS読み込み
info_json = json.dumps(info_data, ensure_ascii=False)

with open("templates/search_js.js", encoding="utf-8") as f:
    search_js = f.read()

search_js = search_js.replace("__INFO_JSON__", info_json)
search_js = "<script>\n" + search_js + "\n</script>\n"


# ---------- HTML生成 ----------

# まず地図HTMLを保存
m.save("index.html")

# 生成された index.html の </body> の直前に検索UIを差し込む
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

insert = search_ui + "\n" + search_js

if "</body>" in html:
    html = html.replace("</body>", insert + "\n</body>")
else:
    print("⚠️ </body> が見つかりませんでした")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
