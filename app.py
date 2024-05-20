from flask import Flask, render_template, request, send_file, flash, redirect, url_for, Response
from PIL import Image, ImageDraw
import os
import math
import re
import datetime
import uuid  # Benzersiz dosya adları için ekledik

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Flash mesajları için gerekli

# Çiçek resimlerinin bulunduğu dizin yolu (transparan arka planlı resimler)
FLOWER_DIR = os.path.join('static', 'flowers')

# İsme göre çiçek resmi oluşturan fonksiyon
def generate_flower_bouquet(name, transparent=True):
    print(f"Generating bouquet for name: {name}")

    # Her harfe karşılık gelen çiçek resimlerini yükle
    flower_images = []
    for letter in name:
        flower_path = os.path.join(FLOWER_DIR, f"{letter.upper()}.png")
        if os.path.exists(flower_path):
            try:
                flower_images.append(Image.open(flower_path))
                print(f"Loaded image for letter: {letter.upper()}")
            except Exception as e:
                print(f"Error loading image for letter {letter.upper()}: {e}")
        else:
            print(f"Flower image not found for letter: {letter.upper()}")

    # Çiçek resimlerini yapıştırmak için boş bir tuval oluştur
    canvas_width = 2340
    canvas_height = 1560
    background_color = (255, 255, 255, 0) if transparent else (255, 255, 255, 255)
    canvas = Image.new('RGBA', (canvas_width, canvas_height), background_color)

    # Çiçekleri demet oluşturacak şekilde yerleştir
    num_flowers = len(flower_images)
    center_x = canvas_width // 2 - 100  # Demetin merkezi
    base_y = canvas_height - 700  # Demetin alt kısmı için yer
    radius = 100  # Çiçeklerin yayılma yarıçapı


    for i, flower in enumerate(flower_images):
        angle = (i - (num_flowers - 1) / 2) * (math.pi / (num_flowers if num_flowers > 1 else 1))
        x = center_x + int(radius * math.cos(angle)) - flower.width // 2
        y = base_y - int(radius * math.sin(angle)) - flower.height // 2
        canvas.paste(flower, (x, y), flower)
        print(f"Pasted flower {i + 1}/{num_flowers} at ({x}, {y})")

    # Vazoyu tuvalin alt merkezine çiz
    vase = Image.open('static/vase.png')  # Vazo resmi yükleyin
    vase_width, vase_height = vase.size
    vase_x = (canvas_width - vase_width) // 2 - 50
    vase_y = base_y - vase_height + 600  # Vazoyu biraz daha yukarı taşıdık
    canvas.paste(vase, (vase_x, vase_y), vase)
    print(f"Pasted vase at ({vase_x}, {vase_y})")

    # Benzersiz dosya adı oluştur
    unique_id = uuid.uuid4().hex

    output_path = os.path.join('static', 'output', f'flower_bouquet_{unique_id}_{"transparent" if transparent else "normal"}.png')

    output_path = os.path.join('static', 'output',
                               f'flower_bouquet_{unique_id}_{"transparent" if transparent else "normal"}.png')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path, format='PNG')

    print(f"Bouquet image saved to: {output_path}")
    return output_path


@app.route('/', methods=['GET', 'POST'])
def index():
    image_path_transparent = None
    image_path_normal = None
    name = None
    if request.method == 'POST':
        name = request.form['name']
        if not re.match("^[a-zA-Z]+$", name):
            flash('Lütfen sadece İngilizce karakterler kullanın ve boşluk bırakmayın.')
            return redirect(url_for('index'))
        image_path_transparent = generate_flower_bouquet(name, transparent=True)
        image_path_normal = generate_flower_bouquet(name, transparent=False)
    return render_template('index.html', image_path_transparent=image_path_transparent,
                           image_path_normal=image_path_normal, name=name)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(filename, as_attachment=True)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []
    ten_days_ago = (datetime.datetime.now() - datetime.timedelta(days=10)).date().isoformat()

    # Mevcut rotalarınızı ekleyin
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(
                ["https://cicekalfabesi.com" + str(rule.rule), ten_days_ago]
            )

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = Response(sitemap_xml, mimetype='application/xml')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))




>>>>>>> Stashed changes
