import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from PIL import Image
from io import BytesIO
import math
from dotenv import load_dotenv
import os

# .envファイルを読み込む
load_dotenv()

# Spotify APIの認証情報を環境変数から取得
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')

# 認証
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# プレイリストID
playlist_id = PLAYLIST_ID

# プレイリストのトラックを取得
results = sp.playlist_tracks(playlist_id)
tracks = results['items']

# 画像URLのリスト
image_urls = []

while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

for item in tracks:
    track = item['track']
    if track['album']['images']:
        image_urls.append(track['album']['images'][0]['url'])

# 画像のダウンロードと正方形画像への加工
images = []

for url in image_urls:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((100, 100))  # サイズは適宜調整してください
    images.append(img)

# 画像の数に応じた列数を計算し、モザイク画像を作成
def create_square_mosaic(images):
    num_images = len(images)
    num_cols = int(math.sqrt(num_images))
    num_rows = math.ceil(num_images / num_cols)
    width, height = images[0].size
    mosaic_size = min(num_cols, num_rows)
    
    mosaic = Image.new('RGB', (mosaic_size * width, mosaic_size * height))

    for index, img in enumerate(images[:mosaic_size * mosaic_size]):
        row, col = divmod(index, mosaic_size)
        mosaic.paste(img, (col * width, row * height))

    return mosaic

# モザイク画像を作成
mosaic_image = create_square_mosaic(images)
mosaic_image.save('mosaic_image.jpg')
mosaic_image.show()
