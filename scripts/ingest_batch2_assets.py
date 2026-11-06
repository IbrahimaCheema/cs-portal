import os
import sys
import ssl
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

dest_dir = r"C:\Projects\antigravity-ide\cs-portal\public\images\batch2"
os.makedirs(dest_dir, exist_ok=True)

images = [
    # About Us
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/about-1.jpg", "about-1.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/about-2.jpg", "about-2.jpg"),
    
    # Mission & Values
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/value-mission.jpg", "value-mission.jpg"),
    
    # History
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/06/crescent-history-u.jpg", "crescent-history-u.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/09/first-batch.jpg", "first-batch.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/06/crescent-hint-college.jpg", "crescent-hint-college.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/nonprofit.jpg", "nonprofit.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2022/02/DJI_0043.jpg", "DJI_0043.jpg"),

    # Affiliations
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/bise.png", "bise.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/12/british.jpg", "british.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/toastmaster.png", "toastmaster.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/12/cambridge.jpg", "cambridge.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/12/WWF-Pakistyan.jpg", "WWF-Pakistyan.jpg"),

    # Board of Trustees
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/06/Justice-R-Karamat-Nazir-Bhandari.png", "Justice-R-Karamat-Nazir-Bhandari.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Mr.-Ahsan-Bashir.png", "Mr.-Ahsan-Bashir.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Mr.-Altaf-Muhammad-Saleem.png", "Mr.-Altaf-Muhammad-Saleem.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Ms.-Attiya-Inayatullah.png", "Ms.-Attiya-Inayatullah.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Mr.-Humayun-Mazhar.png", "Mr.-Humayun-Mazhar.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Mr.-Muhammad-Anwar.png", "Mr.-Muhammad-Anwar.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Mr.-Nasir-Bashir.png", "Mr.-Nasir-Bashir.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Mr.-Salman-Altaf-Saleem.png", "Mr.-Salman-Altaf-Saleem.png"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/04/Mr.-Tariq-Bashir.png", "Mr.-Tariq-Bashir.png"),

    # Administration key portraits
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/Ms-Rabia-Najam-Principal.jpg", "Ms-Rabia-Najam-Principal.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/Ms-Zenab-Ali-IB-PYP-Coordinator.jpg", "Ms-Zenab-Ali-IB-PYP-Coordinator.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/Ms-Maliha-Athar-Senior-Headmistress.jpg", "Ms-Maliha-Athar-Senior-Headmistress.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/Ms-Shazia-Shahid-Gardezi-Headmistress.jpg", "Ms-Shazia-Shahid-Gardezi-Headmistress.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/Ms-Maria-Khalid-Art-Coordinator.jpg", "Ms-Maria-Khalid-Art-Coordinator.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/Mr-Suleman-Zafar-Principal-Senior-Boys.jpg", "Mr-Suleman-Zafar-Principal-Senior-Boys.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/Mr-Waqas-Ahmad-Khan-Headmaster.jpg", "Mr-Waqas-Ahmad-Khan-Headmaster.jpg")
]

success = 0
for url, filename in images:
    filepath = os.path.join(dest_dir, filename)
    if os.path.exists(filepath):
        print(f"Already exists: {filename}")
        success += 1
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            with open(filepath, "wb") as f:
                f.write(data)
        print(f"✓ Downloaded: {filename} ({len(data)} bytes)")
        success += 1
    except Exception as e:
        print(f"❌ Failed: {filename}: {e}")

print(f"\nDone: {success}/{len(images)} images ready.")
