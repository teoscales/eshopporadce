"""Vlastní hostování písem (bez Google Fonts): z @fontsource vybere latin a latin-ext woff2 do public/fonts."""
import re, shutil, sys, pathlib
SRC = pathlib.Path(sys.argv[1])  # cesta k node_modules/@fontsource
OUT = pathlib.Path(__file__).resolve().parent.parent / "public" / "fonts"
FAMS = {"domine": [500, 600, 700], "nunito-sans": [400, 600, 700, 800], "outfit": [500, 600, 700],
        "space-grotesk": [400, 500, 600, 700], "jetbrains-mono": [400, 600]}
OUT.mkdir(parents=True, exist_ok=True)
css = ["/* Písma hostovaná přímo na eshop-poradce.eu (licence SIL OFL), žádné spojení s Google. */"]
for fam, weights in FAMS.items():
    for w in weights:
        for sub in ("latin-ext", "latin"):
            block = (SRC / fam / f"{sub}-{w}.css").read_text()
            block = re.sub(r",\s*url\([^)]+\.woff\) format\('woff'\)", "", block)
            for f in re.findall(r"\./files/([\w.-]+\.woff2)", block):
                shutil.copy(SRC / fam / "files" / f, OUT / f)
            css.append(block.replace("./files/", "/fonts/").strip())
(OUT / "fonts.css").write_text("\n".join(css) + "\n")
print(len(list(OUT.glob("*.woff2"))), "souborů")
