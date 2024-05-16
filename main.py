import os
from PIL import Image

def make_background_transparent(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")

    datas = image.getdata()

    new_data = []
    for item in datas:
        # Beyaz arka planı kontrol et
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    image.save(output_path, "PNG")

# Çiçek resimlerinin bulunduğu dizin
flower_dir = 'static/flowers'

# Transparan arka planlı çiçek resimleri için çıktı dizini
output_dir = 'static/flowers_transparent'
os.makedirs(output_dir, exist_ok=True)

# Tüm çiçek resimlerini işleyip kaydet
for file_name in os.listdir(flower_dir):
    if file_name.endswith('.png'):
        make_background_transparent(os.path.join(flower_dir, file_name), os.path.join(output_dir, file_name))

print("Tüm çiçek resimleri arka planı transparan yapılarak kaydedildi.")
