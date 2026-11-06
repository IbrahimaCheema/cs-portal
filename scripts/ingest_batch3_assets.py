import os
import sys
import ssl
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

dest_dir = r"C:\Projects\antigravity-ide\cs-portal\public\images\batch3"
os.makedirs(dest_dir, exist_ok=True)

images = [
    # Early Years & Primary
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/redcoat.jpg", "redcoat.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/red2.jpg", "red2.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/chairs.jpg", "chairs.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/junior.jpg", "junior.jpg"),
    
    # Middle School
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/5px.jpg", "5px.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/09/6px.jpg", "6px.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/12/writeup.png", "writeup.png"),
    
    # IB Programmes
    ("https://crescentschool.edu.pk/wp-content/uploads/2026/07/IB-DP-300x132.jpg", "IB-DP-300x132.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2026/07/Admission-Open-Poster-1-1024x1024.png", "ib_admission_poster.png"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2026/07/IB-CP-300x107.jpg", "IB-CP-300x107.jpg"),
    
    # Senior School
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/09/lab.jpg", "lab.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2020/11/senior.jpg", "senior.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/09/basketball.jpg", "basketball.jpg"),
    ("https://crescentschool.edu.pk/wp-content/uploads/2021/07/senior-a.jpg", "senior-a.jpg"),
    
    # Cambridge Section
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2020/11/cambridge.jpg", "cambridge_sec.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/07/creb1.jpg", "creb1.jpg"),
    
    # The Crescent College
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/07/bg-10.jpg", "college_bg10.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/07/bh-10.jpg", "college_bh10.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2021/07/bg-100.jpg", "college_bg100.jpg"),
    
    # Facilities
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/well-ventilated-classrooms-junior.jpg", "classrooms_junior.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/gym.jpg", "gym.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/swimming-pool.jpg", "swimming_pool.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/tennis-court.jpg", "tennis_court.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/library-college.jpg", "library_college.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/blue-ip.jpg", "blue_ip.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/computer-lab.jpg", "computer_lab.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/lecture-theater.jpg", "lecture_theater.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/Clicnic.jpg", "clinic.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/training-centre.jpg", "training_centre.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/1Y5A2488-F-1.jpg", "science_lab.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/mosque.jpg", "mosque.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/01/green-lush.jpg", "sports_grounds.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/auditorium.jpg", "auditorium.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2022/02/daycare.jpg", "daycare.jpg"),
    ("https://www.crescentschool.edu.pk/wp-content/uploads/2023/10/robotics.jpg", "robotics.jpg")
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
