import folium
import json
import base64

# GeoJSON読み込み
with open("prefectures.geojson", encoding="utf-8") as f:
    geo_json = json.load(f)

visited = ["北海道", "東京都", "京都府", "沖縄県"]

# 複数写真＋詳細テキスト
info_data = {
    "北海道": {
        "images": ["akw1.jpg", "akw2.jpg", "akw3.jpg"],
        "text": "北海道：自然豊かで食べ物が美味しい地域。観光名所や温泉も豊富です。"
    },
    "沖縄県": {
        "images": ["oka1.jpg", "oka2.jpg"],
        "text": "沖縄県：美しい海と独自文化。琉球王国の歴史も楽しめます。"
    },
}

# 地図作成
m = folium.Map(location=[37.5, 137], zoom_start=5, control_scale=True, height=900)

# 色分け関数
def style_function(feature):
    name = feature["properties"]["name"]
    if name in visited:
        return {"fillColor": "green", "color": "black", "weight": 1, "fillOpacity": 0.7}
    else:
        return {"fillColor": "lightgray", "color": "black", "weight": 1, "fillOpacity": 0.3}

def highlight_function(feature):
    return {"fillColor": "yellow", "color": "orange", "weight": 3, "fillOpacity": 0.9}

# 通常ポップアップ（地図上1枚表示）
def popup_html(name):
    if name in info_data:
        img_path = info_data[name]["images"][0]  # 最初の画像のみ
        text = info_data[name]["text"]
        encoded = base64.b64encode(open(img_path, "rb").read()).decode()
        html = f"""
        <div style="width:200px">
            <img src="data:image/jpeg;base64,{encoded}" width="180"><br>
            <p>{text}</p>
        </div>
        """
        return html
    else:
        return f"<b>{name}</b>（情報なし）"

# GeoJSON追加
for feature in geo_json["features"]:
    name = feature["properties"]["name"]
    popup = folium.Popup(popup_html(name), max_width=250)

    gj = folium.GeoJson(
        feature,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(fields=["name"], labels=False),
    )
    gj.add_child(popup)
    gj.add_to(m)

    # ダブルクリックでモーダル表示用 JavaScript
    images = info_data.get(name, {}).get("images", [])
    text = info_data.get(name, {}).get("text", "")
    img_base64_list = [base64.b64encode(open(img, "rb").read()).decode() for img in images]

    js_code = f"""
    <script>
    var layer = {gj.get_name()};
    layer.on('dblclick', function(e) {{
        var modal = document.createElement('div');
        modal.id = 'modal';
        modal.style.position = 'fixed';
        modal.style.top = '0'; modal.style.left = '0';
        modal.style.width = '100%'; modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
        modal.style.display = 'flex'; modal.style.justifyContent = 'center'; modal.style.alignItems = 'center';
        modal.style.zIndex = '10000';

        var content = document.createElement('div');
        content.style.backgroundColor = 'white'; content.style.padding = '10px';
        content.style.maxWidth = '80%'; content.style.maxHeight = '80%'; content.style.overflow = 'auto';

        var closeBtn = document.createElement('button');
        closeBtn.innerHTML = '閉じる';
        closeBtn.onclick = function(){{ document.body.removeChild(modal); }};
        content.appendChild(closeBtn);

        // 写真スライダー
        var imgs = {img_base64_list};
        var imgTag = document.createElement('img');
        imgTag.src = 'data:image/jpeg;base64,' + imgs[0];
        imgTag.style.maxWidth = '100%';
        content.appendChild(imgTag);

        if(imgs.length > 1){{
            var index = 0;
            var nextBtn = document.createElement('button');
            nextBtn.innerHTML = '次の写真';
            nextBtn.onclick = function(){{
                index = (index + 1) % imgs.length;
                imgTag.src = 'data:image/jpeg;base64,' + imgs[index];
            }};
            content.appendChild(nextBtn);
        }}

        // 詳細テキスト
        var p = document.createElement('p');
        p.innerHTML = "{text}";
        content.appendChild(p);

        modal.appendChild(content);
        document.body.appendChild(modal);
    }});
    </script>
    """
    gj.add_child(folium.Element(js_code))

# 高さ調整
m.get_root().html.add_child(folium.Element("""
<style>
html, body {{height:100%; margin:0;}}
#map {{height:100%; width:100%;}}
</style>
"""))

# 保存
m.save("index.html")
