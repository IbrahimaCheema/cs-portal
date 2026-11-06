import os
import sys
import ssl
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

dest_dir = r"C:\Projects\antigravity-ide\cs-portal\public\images\batch5"
os.makedirs(dest_dir, exist_ok=True)

images = [
    # Cambridge & Global Certifications
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Cambridge-Logo-300x91.png", "cambridge_pdq_logo.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/11/Celta-1.jpg", "celta_1.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/11/Celta-2.jpg", "celta_2.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/11/Delta.jpg", "delta.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/11/Flash.jpg", "flash_leadership.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/TT-logos-1024x128.jpg", "tt_logos.jpg"),
    
    # Training Workshops & Seminars
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/1.jpg", "cpd_workshop_1.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/3.jpg", "cpd_workshop_3.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/4.jpg", "cpd_workshop_4.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/5.jpg", "cpd_workshop_5.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/6.jpg", "cpd_workshop_6.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/7.jpg", "cpd_workshop_7.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/9.jpg", "cpd_workshop_9.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/10.jpg", "cpd_workshop_10.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/11.jpg", "cpd_workshop_11.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/IMG_0543.jpg", "cpd_img_0543.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/IMG_0541.jpg", "cpd_img_0541.jpg")
]

success = 0
for url, filename in images:
    fp = os.path.join(dest_dir, filename)
    if os.path.exists(fp):
        success += 1
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
            with open(fp, "wb") as f:
                f.write(r.read())
        print(f"✓ OK: {filename}")
        success += 1
    except Exception as e:
        print(f"❌ Failed: {filename}: {e}")

print(f"\nDone: {success}/{len(images)} images ready in {dest_dir}.")
