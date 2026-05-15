# saged.club audits — 2026-05-11T15:25:01Z

## 1. Cookie consent audit

### Initial pageload (no consent)
- ✅ No `fbevents.js` script tag in static HTML (good — Pixel loads via JS only after consent)
- ✅ No `fbq('init')` in static HTML
- ✅ `initTracking()` function exists in script.js
- ✅ Pixel ID (1533639615120579) present in script.js, but gated behind `setConsent('accepted')`
- ✅ Consent banner HTML present (`<div id="consent">`)

### Third-party scripts in HTML
```
src="https://maps.google.com/maps?q=Saged,%20C%2F%20de%20les%20Cuines,%208,%2046001%20Val%C3%A8ncia&output=embed"
```

## 2. Lighthouse audit (mobile)

Running PageSpeed Insights API...
PSI parse error: Expecting value: line 1 column 1 (char 0)
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 293, in load
    return loads(fp.read(),
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 25, in <module>
NameError: name 'd' is not defined

---
_Generated Mon May 11 17:25:02 CEST 2026_
