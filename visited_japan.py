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
                   "images/hokkaido/hokkaido03.jpg",
                   ],
        "text": "北海道：海鮮(イクラ、ウニ、カニ)・ジンギスカン・スープカレー・味噌ラーメン",
        "tags": ["#nature", "#旭岳", "#狼犬の森"],
        },
    "東京都": {
        "images": ["images/tokyo/tokyo01.jpg",
                   "images/tokyo/tokyo02.jpg",
                   ],
        "text": "東京都：もんじゃ焼き・寿司",
        "tags": ["#skytree"],
    },
    "京都府": {
        # "images": ["images/kyoto/kyoto01.jpg"],
        "text": "京都府：抹茶・湯豆腐・八つ橋",
        "tags": ["#清水寺"],
    },
    "沖縄県": {
        "images": ["images/okinawa/okinawa01.jpg",
                   "images/okinawa/okinawa02.jpg",
                   ],
        "text": "沖縄県：沖縄そば・海ぶどう",
        "tags": ["#sea","#恩納村","#scuvadiving",],
    },
    "神奈川県": {
        "images": ["images/kanagawa/kanagawa01.jpg",
                   "images/kanagawa/kanagawa02.jpg",
                   "images/kanagawa/kanagawa03.jpg",
                   
                   ],
        "text": "神奈川県：湘南・横浜中華街",
        "tags": ["#座間ひまわり","#mt.fuji","#大観山","#大涌谷"],
    },
    "長野県": {
        "images": ["images/nagano/nagano01.jpg",
                   "images/nagano/nagano02.jpg"],

        "text": "長野県：信州そば",
        "tags": ["#白馬","#八方尾根","#地獄谷温泉"],
    },
    "福岡県": {
        "images": ["images/fukuoka/fukuoka01.jpg",
                   "images/fukuoka/fukuoka02.jpg",
                   ],
        "text": "福岡県：博多ラーメン・もつ鍋",
        "tags": ["#いちご狩り","#北九州","#平尾台"],
    },
    "熊本県": {
        "images": ["images/kumamoto/kumamoto01.jpg",
                   "images/kumamoto/kumamoto02.jpg"
                   "images/kumamoto/kumamoto03.jpg"
                   ],
        "text": "熊本県：馬刺し",
        "tags": ["#mt.aso","#くまもん","#mt.kujyu"],
    },
    "山口県": {
        "images": ["images/yamaguchi/yamaguchi01.jpg",
                   "images/yamaguchi/yamaguchi02.jpg",
                   "images/yamaguchi/yamaguchi03.jpg",               
                   ],
        "text": "山口県：ふぐ",
        "tags": ["#角島","#秋吉台","#唐戸市場"],
    },
    "静岡県": {
        "images": ["images/shizuoka/shizuoka01.jpg",
                   "images/shizuoka/shizuoka02.jpg"],
        "text": "静岡県：うなぎ・しらす",
        "tags": ["#富士山","#mt.fuji"],
    },
    "大分県": {
        "images": ["images/oita/oita01.jpg",
                   "images/oita/oita02.jpg",
                   "images/oita/oita03.jpg",      
                 ],
        "text": "大分県：とり天・温泉",
        "tags": ["#別府温泉","#鶴見岳"],
    },
    "広島県": {
        "images": ["images/hiroshima/hiroshima01.jpg",
                   "images/hiroshima/hiroshima02.jpg"
                   "images/hiroshima/hiroshima03.jpg"
                   ],
        "text": "広島県：広島焼き・牡蠣",
        "tags": ["#宮島","#厳島神社","#deers"],
    },
    "鳥取県": {
        "images": ["images/tottori/tottori01.jpg",
                   ],
        "text": "鳥取県：砂丘・梨",
        "tags": ["#水木しげるロード","#境港"],
    },
    "栃木県": {
        "images": ["images/tochigi/tochigi01.jpg"],
        "text": "栃木県：いちご",
        "tags": ["#mt.natshdake"],
    },
    "大阪府": {
        "images": ["images/osaka/osaka01.jpg"],
        "text": "大阪府：たこ焼き・お好み焼き",
        "tags": ["#大阪城"],
    },
    "兵庫県": {
        # "images": ["images/hyogo/hyogo01.jpg"],
        "text": "兵庫県：神戸牛",
        "tags": ["#姫路城"],
    },
    "奈良県": {
        # "images": ["images/nara/nara01.jpg"],
        "text": "奈良県：柿の葉寿司",
        "tags": ["#東大寺"],
    },
    "宮城県": {
        "images": ["images/miyagi/miyagi01.jpg",
                   "images/miyagi/miyagi02.jpg"
                   ],
        "text": "宮城県：牛タン",
        "tags": ["#きつね村","#牛タン",],
    },
    "岐阜県": {
        "images": ["images/gifu/gifu01.jpg"],
        "text": "岐阜県：飛騨牛",
        "tags": ["#白川郷"],
    },
    "愛知県": {
        # "images": ["images/aichi/aichi01.jpg"],
        "text": "愛知県：味噌カツ",
        "tags": ["#名古屋城"],
    },
    "千葉県": {
        # "images": ["images/chiba/chiba01.jpg"],
        "text": "千葉県：落花生",
        "tags": ["#ディズニー"],
    },
    "山梨県": {
        "images": ["images/yamanashi/yamanashi01.jpg",
                   "images/yamanashi/yamanashi02.jpg"
                   ],
        "text": "山梨県：ほうとう",
        "tags": ["#富士山","#mt.fuji",],
    },
    "群馬県": {
        # "images": ["images/gunma/gunma01.jpg"],
        "text": "群馬県：焼きまんじゅう",
        "tags": ["#草津温泉"],
    },
    "茨城県": {
        "images": ["images/ibaraki/ibaraki01.jpg",
                   "images/ibaraki/ibaraki02.jpg",
                   ],
        "text": "茨城県：筑波山/877m",
        "tags": ["#mt.tukuba",],
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

