import os
import sys
import ssl
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

dest_dir = r"C:\Projects\antigravity-ide\cs-portal\public\images\batch4"
os.makedirs(dest_dir, exist_ok=True)

images = [
    # School of Art
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/09/school-of-arts.jpg", "school-of-arts.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/09/school-of-arts2.jpg", "school-of-arts2.jpg"),

    # School of Music
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/mac.jpg", "music_mac.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/mac2.jpg", "music_mac2.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/gospel.png", "music_gospel.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/karaoke.png", "music_karaoke.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/sheet-music.png", "music_sheet.png"),

    # The Finishing School
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/12/finishing-school.png", "finishing_school_1.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/12/finishing-scholl-2.png", "finishing_school_2.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/12/finishing-school-3.png", "finishing_school_3.png"),

    # Gentlemen's League
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/07/nnn.jpg", "league_nnn.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/league.jpg", "league_main.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/fence.png", "icon_fence.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/target.png", "icon_archery.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/riding.png", "icon_riding.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/golf-field.png", "icon_golf.png"),

    # The Quran School
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/quran.jpg", "quran_main.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/quran-1.jpg", "quran_sub.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/12/quran.png", "quran_icon.png"),

    # Robotics
    ("https://crescentschool.edu.pk/wp-content/uploads/2023/10/HIZ_1422-scaled.jpg", "robotics_lab_1.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2023/10/HIZ_1398-1-scaled.jpg", "robotics_lab_2.jpg")
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
