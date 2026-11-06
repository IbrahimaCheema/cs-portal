import os
import sys
import ssl
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ASSET_MAP = {
    "mont.jpg": "https://crescentschool.edu.pk/wp-content/uploads/2020/12/mont.jpg",
    "eligible_junior.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/eligible-junior-2.jpg",
    "eligible_middle.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/1Y5A0024-F-1.jpg",
    "eligible_senior.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/1Y5A0126-F.jpg",
    "eligible_cambridge.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/1Y5A0155-F.jpg",
    "eligible_college.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/1Y5A0207-F.jpg",
    "student_activity_1.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/1Y5A1675-F2.jpg",
    "student_activity_2.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/1Y5A2351-F.jpg",
    "admission_office.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/ARK_5351-F-1.jpg",
    "library_study.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/ARK_5929-F.jpg",
    "science_lab.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/DSC_9594-ff-2.jpg",
    "merit_k2.jpeg": "https://www.crescentschool.edu.pk/wp-content/uploads/2024/02/K2_Merit-List_Annoucement-1024x948.jpeg",
    "merit_nursery.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2024/02/nursery-merit-list-poster-e1675914546508.jpg",
    "merit_pg.jpeg": "https://www.crescentschool.edu.pk/wp-content/uploads/2024/02/pg-merit-list-1008x1024.jpeg",
    "merit_class2.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-2-1024x1024.jpg",
    "merit_class3.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-3-1024x1024.jpg",
    "merit_class4.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-4-1024x1024.jpg",
    "merit_class5.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-5-1024x1024.jpg",
    "merit_class6.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-6-1024x1024.jpg",
    "merit_class7.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-7-1024x1024.jpg",
    "merit_class8.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-8-1024x1024.jpg",
    "merit_class9.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/Class-9-1024x1024.jpg",
    "merit_myp1.jpg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/MYP-1-1-1024x1024.jpg",
    "merit_poster_1.jpeg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/WhatsApp-Image-2025-03-11-at-3.05.44-PM-1024x1024.jpeg",
    "merit_poster_2.jpeg": "https://www.crescentschool.edu.pk/wp-content/uploads/2025/03/WhatsApp-Image-2025-03-14-at-11.50.18-AM-1024x1024.jpeg",
    "admission_open_poster.png": "https://www.crescentschool.edu.pk/wp-content/uploads/2026/07/Admission-Open-Poster-1-1024x1024.png"
}

out_dir = r"C:\Projects\antigravity-ide\cs-portal\public\images\batch6"
os.makedirs(out_dir, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

success = 0
for filename, url in ASSET_MAP.items():
    dest_path = os.path.join(out_dir, filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"Skipping {filename} (already exists, {os.path.getsize(dest_path)} bytes)")
        success += 1
        continue
    
    print(f"Downloading {filename} from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            content = resp.read()
            with open(dest_path, 'wb') as f:
                f.write(content)
            print(f"  ✓ Saved {filename} ({len(content)} bytes)")
            success += 1
    except Exception as e:
        print(f"  ❌ Error downloading {filename}: {e}")

print(f"\nAsset Ingestion Complete: {success}/{len(ASSET_MAP)} downloaded to {out_dir}")
