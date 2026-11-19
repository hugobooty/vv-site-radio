"""Copy the rendered songs from projects/vulpine-valley/ost/site-radio ("05 Foxfire Rally (drop).mp3") into this
folder under the names the site player asks for ("foxfire-kick.mp3")."""
import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "vulpine-valley", "ost", "site-radio")
IDS = ["valley", "lantern", "pond", "petal", "foxfire", "ribbon", "rain", "velvet", "candy", "hilltop", "moth", "sugar", "tea", "lastlight"]
n = 0
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".mp3"): continue
    k = int(f[:2]) - 1; mix = "kick" if "(drop)" in f else "calm"
    shutil.copy2(os.path.join(SRC, f), os.path.join(HERE, f"{IDS[k]}-{mix}.mp3")); n += 1
print("copied", n)
