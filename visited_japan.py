import folium
import json

with open("prefectures.geojson", encoding="utf-8") as f:
    geo_json = json.load(f)

visited = ["北海道", "東京都", "京都府", "沖縄県", "宮城県", "栃木県", "神奈川県", "福岡県", "熊本県","山梨県",]

info_data = {
    "北海道": {"img": "akw.jpg", "text": "北海道：自然豊かで食べ物が美味しい地域"},
    "沖縄県": {"img": "oka.jpg", "text": "沖縄県：美しい海と独自文化"},
}

m = folium.Map(location=[37.5, 137], zoom_start=5)

def style_function(feature):
    name = feature["properties"]["name"]
    if name in visited:
        return {"fillColor": "red", "color": "black", "weight": 1, "fillOpacity": 0.7}
    else:
        return {"fillColor": "lightgray", "color": "black", "weight": 1, "fillOpacity": 0.3}

def highlight_function(feature):
    return {"fillColor": "yellow", "color": "orange", "weight": 3, "fillOpacity": 0.9}

def popup_html(name):
    if name in info_data:
        img = info_data[name]["img"]
        text = info_data[name]["text"]
        html = f"""
        <div style="width:200px">
            <img src="{img}" width="180"><br>
            <p>{text}</p>
        </div>
        """
        return html
    else:
        return f"<b>{name}</b>（情報なし）"

# ★★★ ここが重要：GeoJsonPopup を使わず、feature ごとに Popup を付ける
for feature in geo_json["features"]:
    html = popup_html(feature["properties"]["name"])
    popup = folium.Popup(html, max_width=250)

    folium.GeoJson(
        feature,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["name"],
            labels=False
        ),
        popup=popup
    ).add_to(m)


m.save("visited_map.html")