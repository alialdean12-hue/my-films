"""Makes text easy to pronounce for Arabic TTS (used automatically by tts_edge.py).
- numbers -> Arabic words (1912 -> ألف وتسعمئة واثنا عشر, 3.5 -> ثلاثة فاصلة خمسة, 70% -> سبعون بالمئة, 1,000,000 -> مليون)
- Latin names -> Arabic spelling from pronounce.json (studio-kit/scripts/pronounce.json, add your own words)
- symbols: % ° km kg $ € → words
  python3 arabic_speech.py "عام 1912 غرقت Titanic بنسبة 70%"   (prints the spoken form)"""
import json, os, re, sys
ONES = ["", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة", "عشرة", "أحد عشر", "اثنا عشر", "ثلاثة عشر", "أربعة عشر", "خمسة عشر", "ستة عشر", "سبعة عشر", "ثمانية عشر", "تسعة عشر"]
TENS = ["", "", "عشرون", "ثلاثون", "أربعون", "خمسون", "ستون", "سبعون", "ثمانون", "تسعون"]
HUND = ["", "مئة", "مئتان", "ثلاثمئة", "أربعمئة", "خمسمئة", "ستمئة", "سبعمئة", "ثمانمئة", "تسعمئة"]
SCALES = [("", "", "", ""), ("ألف", "ألفان", "آلاف", "ألف"), ("مليون", "مليونان", "ملايين", "مليون"), ("مليار", "ملياران", "مليارات", "مليار")]
def below_1000(n):
    h, r = divmod(n, 100); parts = []
    if h: parts.append(HUND[h])
    if r:
        if r < 20: parts.append(ONES[r])
        else:
            t, o = divmod(r, 10); parts.append((ONES[o] + " و" if o else "") + TENS[t])
    return " و".join(parts)
def number_words(n):
    if n == 0: return "صفر"
    if n < 0: return "سالب " + number_words(-n)
    groups = []; k = 0
    while n:
        n, g = divmod(n, 1000)
        if g:
            one, two, few, many = SCALES[k]
            if k == 0: w = below_1000(g)
            elif g == 1: w = one
            elif g == 2: w = two
            elif 3 <= g <= 10: w = below_1000(g) + " " + few
            else: w = below_1000(g) + " " + many
            groups.append(w)
        k += 1
    return " و".join(reversed(groups))
DIG = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
def load_dict():
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pronounce.json")
    try: return json.load(open(f, encoding="utf-8"))
    except Exception: return {}
UNITS = {"%": " بالمئة", "°": " درجة", "km": " كيلومتر", "كم": " كيلومتر", "kg": " كيلوغرام", "$": " دولار", "€": " يورو", "m": " متر", "cm": " سنتيمتر"}
def speakable(text, extra=None):
    d = load_dict(); d.update(extra or {})
    for k in sorted(d, key=len, reverse=True): text = re.sub(rf"(?<![\w]){re.escape(k)}(?![\w])", d[k], text, flags=re.I)
    text = text.translate(DIG)
    text = re.sub(r"\$\s?(\d[\d,]*(?:\.\d+)?)", r"\1$", text)
    def num(m):
        s, unit = m.group(1).replace(",", ""), m.group(2) or ""
        if "." in s: a, b = s.split("."); w = number_words(int(a)) + " فاصلة " + " ".join(number_words(int(c)) for c in b) if len(b) > 2 else number_words(int(a)) + " فاصلة " + number_words(int(b))
        else: w = number_words(int(s))
        return w + UNITS.get(unit.strip(), "")
    text = re.sub(r"(?<![0-9A-Za-z.])-(?=\d)", "سالب ", text)
    text = re.sub(r"(?<![0-9A-Za-z.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?:\s?(%|°|km|kg|cm|m\b|\$|€|كم\b))?", num, text)
    return re.sub(r"\s+", " ", text).strip()
if __name__ == "__main__":
    print(speakable(" ".join(sys.argv[1:]) or __doc__))
