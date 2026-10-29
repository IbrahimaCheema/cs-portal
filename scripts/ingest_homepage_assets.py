import os
import sys
import urllib.request
import ssl

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

images = [
    # Logos
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/01/Crescent-Logo-1-1.png", "cs_logo.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2023/11/Crescent-Early-Years-logo.png", "logo_early_years.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/01/school-logo.png", "logo_school.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/01/college-logo.png", "logo_college.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/01/o-a-logo.png", "logo_cambridge.png"),
    
    # Hero Slider Images
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2024/09/DJI_20240409085743_0704_D.jpg", "hero_slider_1.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2024/09/Boys-College-Building-f.jpg", "hero_slider_2.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2024/09/DJI_20240409091648_0722_D-f-low.jpg", "hero_slider_3.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2024/09/80-girls-buildign.png", "hero_slider_4.png"),
    
    # Welcome & Campus Features
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/08/Crescent-Early-Years-f.jpg", "welcome_early_years.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/09/side.jpg", "welcome_side.jpg"),
    
    # High Achievements Posters / Highlights
    ("https://crescentschool.edu.pk/wp-content/uploads/2026/09/WhatsApp-Image-2026-09-16-at-11.25.21-AM-1024x1024.jpeg", "achievement_1.jpeg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2026/09/WhatsApp-Image-2026-09-16-at-9.22.05-AM-1024x1019.jpeg", "achievement_2.jpeg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2026/09/WhatsApp-Image-2026-09-16-at-9.18.32-AM-1024x1024.jpeg", "achievement_3.jpeg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2026/09/WhatsApp-Image-2026-09-24-at-11.00.42-AM-1024x1024.jpeg", "achievement_4.jpeg"),
    
    # Affiliations & Partners
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/gavel-150x132.png", "partner_gavel.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/dsp-150x133.png", "partner_dsp.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/rizq-150x133.png", "partner_rizq.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/pearson-150x132.png", "partner_pearson.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/orange-150x132.png", "partner_orange.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/itti-150x132.png", "partner_itti.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/iml-150x132.png", "partner_iml.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/icots-150x132.png", "partner_icots.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/alliance-150x132.png", "partner_alliance.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/09/usefp-150x133.png", "partner_usefp.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2024/03/IB-Logo-f-150x130.jpg", "partner_ib.jpg")
]

dest_dir = r"C:\Projects\antigravity-ide\cs-portal\public\images"
os.makedirs(dest_dir, exist_ok=True)

for url, filename in images:
    filepath = os.path.join(dest_dir, filename)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            data = resp.read()
            with open(filepath, "wb") as f:
                f.write(data)
        print(f"✓ Downloaded: {filename} ({len(data)} bytes)")
    except Exception as e:
        print(f"❌ Failed {filename} ({url}): {e}")

print("\nAsset ingestion complete.")
