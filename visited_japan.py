import folium          # Folium（地図描画ライブラリ）を読み込む
import json            # JSONファイルを扱うための標準ライブラリ
import base64          # 画像をBase64形式に変換するためのライブラリ

# 都道府県境界データ（GeoJSON）を読み込む
with open("prefectures.geojson", encoding="utf-8") as f:
    geo_json = json.load(f)

# 訪問済みの都道府県リスト
visited = ["北海道", "東京都", "京都府", "沖縄県", "宮城県", "栃木県", "神奈川県", "福岡県", "熊本県", "山梨県"]

# 各都道府県のポップアップ情報（画像と説明文）
info_data = {
    "北海道": {"img": "akw.jpg", "text": "北海道：自然豊かで食べ物が美味しい地域"},
    "沖縄県": {"img": "oka.jpg", "text": "沖縄県：美しい海と独自文化"},
}

# 地図の基本設定（中心位置、ズーム、操作制限など）
m = folium.Map(
    location=[37.5, 137],     # 日本の中心付近
    zoom_start=5,             # 初期ズームレベル
    control_scale=True,       # スケールバーを表示
    zoom_control=False,       # ズームボタンを非表示
    dragging=False,           # ドラッグで移動できないようにする
    scrollWheelZoom=False,    # ホイールズームを無効化
    doubleClickZoom=False     # ダブルクリックズームを無効化
)

# 都道府県の色付けルール（訪問済みかどうかで色を変える）
def style_function(feature):
    name = feature["properties"]["name"]  # GeoJSON 内の都道府県名を取得
    if name in visited:
        # 訪問済み → 緑色で塗る
        return {"fillColor": "green", "color": "black", "weight": 1, "fillOpacity": 0.7}
    else:
        # 未訪問 → 薄いグレー
        return {"fillColor": "lightgray", "color": "black", "weight": 1, "fillOpacity": 0.3}

# マウスホバー時のハイライト設定
def highlight_function(feature):
    return {"fillColor": "yellow", "color": "orange", "weight": 3, "fillOpacity": 0.9}

# ポップアップのHTMLを生成する関数
def popup_html(name):
    if name in info_data:
        img_path = info_data[name]["img"]   # 画像ファイル名
        text = info_data[name]["text"]      # 説明文
        encoded = base64.b64encode(open(img_path, "rb").read()).decode()  # 画像をBase64に変換

        # ポップアップに表示するHTML
        html = f"""
        <div style="width:200px">
            <img src="data:image/jpeg;base64,{encoded}" width="180"><br>
            <p>{text}</p>
        </div>
        """
        return html
    else:
        # info_data に登録がない場合
        return f"<b>{name}</b>（情報なし）"

# GeoJSON の各都道府県を地図に追加
for feature in geo_json["features"]:
    name = feature["properties"]["name"]  # 都道府県名
    html = popup_html(name)               # ポップアップHTMLを生成
    popup = folium.Popup(html, max_width=250)  # ポップアップオブジェクトを作成
    
    # GeoJSON レイヤーを作成
    gj = folium.GeoJson(
        feature,
        style_function=style_function,            # 通常時の色
        highlight_function=highlight_function,    # ホバー時の色
        tooltip=folium.GeoJsonTooltip(fields=["name"], labels=False),  # ツールチップ（県名）
    )
    gj.add_child(popup)  # ポップアップを追加
    gj.add_to(m)         # 地図に追加

# 完成した地図をHTMLとして保存
m.save("index.html")