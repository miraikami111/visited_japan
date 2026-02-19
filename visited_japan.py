import folium
import json
import os

# --- Data ---
with open("prefectures.geojson", encoding="utf-8") as f:
    geo_json = json.load(f)

visited = ["北海道", "東京都", "京都府", "沖縄県"]

info_data = {
    "北海道": {
        "images": ["images/akw1.jpg"],
        "text": "北海道：自然豊かで食べ物が美味しい地域。観光名所や温泉も豊富です。"
    },
    "沖縄県": {
        "images": ["images/oka.jpg"],
        "text": "沖縄県：美しい海と独自文化。琉球王国の歴史も楽しめます。"
    },
}

# --- Map (offline: no tiles) ---
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
    if images:
        img_path = images[0]
        if os.path.exists(img_path):
            img_html = f'<img src="{img_path}" width="180"><br>'

    return f"""
    <div style="width:200px">
        <b>{pref_name}</b><br>
        {img_html}
        <p>{text}</p>
    </div>
    """

for feature in geo_json["features"]:
    pref_name = feature["properties"]["name"]

    gj = folium.GeoJson(
        feature,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(fields=["name"], labels=False),
    ).add_to(m)

    # Click popup (simple)
    gj.add_child(folium.Popup(popup_html(pref_name), max_width=260))

    # Dblclick modal (multi images + text) using file paths (no base64)
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
        var imgs = {imgs_js};
        var text = {text_js};

        layer.on('dblclick', function() {{
          // remove existing modal
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
          title.textContent = prefName;
          title.style.margin = '0 0 10px 0';
          content.appendChild(title);

          var closeBtn = document.createElement('button');
          closeBtn.textContent = '閉じる';
          closeBtn.onclick = function() {{ modal.remove(); }};
          closeBtn.style.marginBottom = '10px';
          content.appendChild(closeBtn);

          // image area
          if (imgs.length > 0) {{
            var index = 0;
            var imgTag = document.createElement('img');
            imgTag.src = imgs[0];
            imgTag.style.width = '100%';
            imgTag.style.maxHeight = '55vh';
            imgTag.style.objectFit = 'contain';
            imgTag.style.background = '#111';
            imgTag.style.borderRadius = '8px';
            content.appendChild(imgTag);

            if (imgs.length > 1) {{
              var nextBtn = document.createElement('button');
              nextBtn.textContent = '次の写真';
              nextBtn.style.marginTop = '8px';
              nextBtn.onclick = function() {{
                index = (index + 1) % imgs.length;
                imgTag.src = imgs[index];
              }};
              content.appendChild(nextBtn);
            }}
          }} else {{
            var noImg = document.createElement('div');
            noImg.textContent = '(写真なし)';
            noImg.style.color = '#666';
            content.appendChild(noImg);
          }}

          var p = document.createElement('p');
          p.textContent = text || '';
          p.style.marginTop = '10px';
          content.appendChild(p);

          // click outside to close
          modal.addEventListener('click', function(e) {{
            if (e.target === modal) modal.remove();
          }});

          modal.appendChild(content);
          document.body.appendChild(modal);
        }});
      }})();
    </script>
    """
    gj.add_child(folium.Element(js_code))

m.get_root().html.add_child(folium.Element("""
<style>
  html, body { height:100%; margin:0; }
  #map { height:100vh; width:100vw; }
</style>
"""))

m.save("index.html")
