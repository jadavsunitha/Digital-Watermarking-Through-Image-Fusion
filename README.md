# Digital-Watermarking-Through-Image-Fusion
💧 Digital Watermarking Through Image Fusion
This project is a web-based application built using Flask, OpenCV, and PyWavelets that performs digital image watermarking using a fused image as the host. The goal is to hide a secret image (watermark) inside another image in a way that it is invisible to the human eye but can be extracted later for copyright protection and verification.

# 🔍 Project Description
In this project, users can:

1. Upload two images and fuse them using alpha blending (50%-50%) to generate one combined image.

2. Upload a watermark image (such as a logo), which is then embedded into the fused image using Discrete Wavelet Transform (DWT).

3. Extract the hidden watermark from the watermarked image using a reverse formula.

This process helps in copyright protection, ownership verification, and tamper detection in digital media.

# 🛠️ Technologies Used
* Python

* Flask – Web framework

* OpenCV – Image processing

* NumPy – Matrix operations

* PyWavelets – For DWT and IDWT

* HTML/CSS – Frontend templates

* Base64 – To display images on webpages

# 📷 How It Works
***1. Image Fusion***

* Uses alpha blending (50% weight from each image).

* Formula: Fused Image = 0.5 × Image1 + 0.5 × Image2.

***2. Watermark Embedding***

* Applies DWT to the fused image to get LL, LH, HL, HH sub-bands.

* Embeds watermark in the LL sub-band using:
* Watermarked_LL = LL + α × Watermark (α = 0.02).

* Reconstructs the watermarked image using IDWT.

***3. Watermark Extraction***

* Applies DWT to both fused and watermarked images.

* Extracts watermark using:
* Extracted_WM = (Watermarked_LL - Original_LL) / α.

# ✅ Features
* Easy-to-use web interface

* Invisible watermarking

* Secure and robust watermark embedding

* Wavelet-based technique for higher accuracy


# 🌍 Applications
* Copyright protection in digital media

* Secure medical image sharing

* Satellite and military imaging

* Online education and video watermarking

