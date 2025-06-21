from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import pywt
import base64

app = Flask(__name__)

fused_image_global = None
watermarked_image_global = None

def image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/method-select')
def method_select():
    return render_template('method_select.html')

@app.route('/fuse-page')
def fuse_page():
    return render_template('fuse.html')

@app.route('/fuse', methods=['POST'])
def fuse():
    global fused_image_global
    img1 = request.files['image1']
    img2 = request.files['image2']
    image1 = cv2.imdecode(np.frombuffer(img1.read(), np.uint8), cv2.IMREAD_COLOR)
    image2 = cv2.imdecode(np.frombuffer(img2.read(), np.uint8), cv2.IMREAD_COLOR)
    image1 = cv2.resize(image1, (256, 256))
    image2 = cv2.resize(image2, (256, 256))
    fused = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
    fused_image_global = fused.copy()
    return render_template('fuse.html',
                           img1=image_to_base64(image1),
                           img2=image_to_base64(image2),
                           fused=image_to_base64(fused))

@app.route('/watermark-page')
def watermark_page():
    return render_template('watermark.html')

@app.route('/embed', methods=['POST'])
def embed():
    global fused_image_global, watermarked_image_global
    if fused_image_global is None:
        return "No fused image available. Please fuse images first.", 400
    watermark_file = request.files['watermark']
    wm = cv2.imdecode(np.frombuffer(watermark_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    wm = cv2.resize(wm, (128, 128))
    fused_gray = cv2.cvtColor(fused_image_global, cv2.COLOR_BGR2GRAY)
    fused_gray = cv2.resize(fused_gray, (256, 256))
    coeffs2 = pywt.dwt2(fused_gray, 'haar')
    LL, (LH, HL, HH) = coeffs2
    watermarked_LL = LL + 0.02 * wm
    watermarked_coeffs = (watermarked_LL, (LH, HL, HH))
    watermarked_image = pywt.idwt2(watermarked_coeffs, 'haar')
    watermarked_image = np.clip(watermarked_image, 0, 255).astype(np.uint8)
    watermarked_image_global = watermarked_image.copy()
    return render_template('watermark.html',
                           fused=image_to_base64(fused_image_global),
                           wm=image_to_base64(wm),
                           embedded=image_to_base64(watermarked_image))

@app.route('/extract', methods=['POST'])
def extract():
    global fused_image_global, watermarked_image_global
    if fused_image_global is None or watermarked_image_global is None:
        return "Required images not available. Please fuse and embed first.", 400
    fused_gray = cv2.cvtColor(fused_image_global, cv2.COLOR_BGR2GRAY)
    fused_gray = cv2.resize(fused_gray, (256, 256))
    coeffs2_fused = pywt.dwt2(fused_gray, 'haar')
    LL_orig, _ = coeffs2_fused
    wm_img = cv2.resize(watermarked_image_global, (256, 256))
    coeffs2_watermarked = pywt.dwt2(wm_img, 'haar')
    LL_watermarked, _ = coeffs2_watermarked
    wm_extracted = (LL_watermarked - LL_orig) / 0.02
    wm_extracted = cv2.normalize(wm_extracted, None, 0, 255, cv2.NORM_MINMAX)
    wm_extracted = wm_extracted.astype(np.uint8)
    wm_extracted = cv2.resize(wm_extracted, (128, 128))
    return render_template('watermark.html',
                           extracted=image_to_base64(wm_extracted))

if __name__ == '__main__':
    app.run(debug=True)
