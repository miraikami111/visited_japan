import folium
import json
import os
from branca.element import Html
from folium.features import GeoJsonTooltip


with open("prefectures.geojson", encoding="utf-8") as f:
    geo_json = json.load(f)

visited = ["北海道", "東京都", "京都府", "沖縄県","神奈川県","長野県","福岡県","熊本県",
           "山口県","静岡県","大分県","広島県","鳥取県","栃木県","大阪府","兵庫県","奈良県",
           "宮城県","岐阜県","愛知県","千葉県","山梨県","群馬県","茨城県",
           ]

info_data = {
    "北海道": {
        "images": ["images/hokkaido/hokkaido01.jpg",
                   "images/hokkaido/hokkaido02.jpg",
                   ],
        "text": "北海道：自然豊かで食べ物が美味しい地域。観光名所や温泉も豊富です。",
        "tags": ["#nature", "#food", "#cold"],
        },

    "沖縄県": {
        "images": [
            "images/okinawa/okinawa01.jpg",
             "images/okinawa/okinawa02.jpg",

            ],
        "text": "沖縄県：美しい海と独自文化。琉球王国の歴史も楽しめます。",
        "tags": ["#sea", "#island", "#culture",],
        },
    
    "東京都": {
        "images": [
        "images/tokyo/tokyo01.jpg",
            ],
        "text": "東京都：都会。",
        "tags": ["#skytree", "#capitalcity","#nightview",],
        },

    "山梨県": {
        "images": [
        "images/yamanashi/yamanashi01.jpg",
        "images/yamanashi/yamanashi02.jpg",
            ],
        "text": "山梨県：富士山が見える",
        "tags": ["#mt.fuji","#毛無山","#花の都公園"],
        },
        
    "静岡県":{
        "images": [
        "images/shizuoka/shizuoka01.jpg",
        
            ],
        "text": "静岡県：富士山が見える",
        "tags": ["#mt.fuji", "#白糸の滝","#朝霧高原",],
        },

    "熊本県":{
        "images": [
        "images/kumamoto/kumamoto01.jpg",
        
            ],
        "text": "熊本県：阿蘇山",
        "tags": [ "#阿蘇山","#くまもん",],
        },
    
    "神奈川県":{
        "images": [
        "images/kanagawa/kanagawa01.jpg",
        
            ],
        "text": "神奈川県：湘南",
        "tags": [ "#座間ひまわり","箱根","くろたまご"],
        },
    }
    
m = folium.Map(
    location=[37.5, 137],
    zoom_start=5,
    tiles=None,
    control_scale=True,
)

# ===== カウント =====
visited_count = len(visited)
total_pref = len(geo_json["features"])
percent = round((visited_count / total_pref) * 100, 1)

counter_html = f"""
<div style="
position: fixed;
bottom: 40px;
right: 20px;
background: white;
padding: 8px 14px;
border-radius: 10px;
box-shadow: 0 4px 10px rgba(0,0,0,0.3);
font-weight: bold;
z-index: 9999;
font-size: 16px;
background: linear-gradient(135deg, #ffffff, #e8f6ff);
">
Visited: {visited_count}/{total_pref} ({percent}%)
</div>
"""

m.get_root().html.add_child(folium.Element(counter_html))
# ===== ここまで =====





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
    # 県名だけ（ホバー写真は表示しない）
    return f"<b>{pref_name}</b>"

for feature in geo_json["features"]:
    pref_name = feature["properties"]["name"]

    data = info_data.get(pref_name, {})
    images = data.get("images", [])
    text = data.get("text", "")

    # 画像HTML
    if images and os.path.exists(images[0]):
        img_html = f"<img src='{images[0]}' width='150' style='border-radius:6px; margin-bottom:6px;'>"
    else:
        img_html = "<div style='color:#666'>(情報なし)</div>"


    tooltip_html_str = f"""
        <div style="width:180px;">
            <b>{pref_name}</b><br>
            {img_html}<br>
            <span style="font-size:12px;">{text}</span>
        </div>
    """

    gj = folium.GeoJson(
        feature,
        style_function=style_function,
        highlight_function=highlight_function,
        control=False,
        tooltip=GeoJsonTooltip(
            fields=[],
            aliases=[],
            labels=False,
            sticky=True,
            style=("background-color: white; border: 1px solid black; border-radius: 6px; padding: 6px;"),
            html=tooltip_html_str
        )
    ).add_to(m)

# ===== ここから追加（for ループの外！）=====

# 地図HTMLを書き出す
m.save("index.html")

# templates から UI/JS を読み込んで差し込む
with open("templates/search_ui.html", encoding="utf-8") as f:
    search_ui = f.read()

with open("templates/search_js.js", encoding="utf-8") as f:
    search_js = f.read()

info_json = json.dumps(info_data, ensure_ascii=False)
search_js = search_js.replace("__INFO_JSON__", info_json)

insert = search_ui + "\n<script>\n" + search_js + "\n</script>\n"

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("</body>", insert + "\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Injected templates/search_js.js into index.html")

# ===== 追加ここまで =====
