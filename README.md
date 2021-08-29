# ⚕ pyHES

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/bc0a52a9b57f4c29930cbd6c796f9a8b)](https://www.codacy.com/gh/keyiflerolsun/pyHES/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=keyiflerolsun/pyHES&amp;utm_campaign=Badge_Grade) ![Repo Boyutu](https://img.shields.io/github/repo-size/keyiflerolsun/pyHES) ![Views](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/keyiflerolsun/pyHES&title=Profile%20Views) [![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/keyiflerolsun/pyHES)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyHES)
![PyPI - Status](https://img.shields.io/pypi/status/pyHES)
![PyPI](https://img.shields.io/pypi/v/pyHES)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyHES)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyHES)
![PyPI - License](https://img.shields.io/pypi/l/pyHES)

⚕ **(pyHES)**, **Python** ile **Hayat Eve Sığar** ile ilgili işlemleri yapan bir kütüphane.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/keyiflerolsun/)

## 🚀 Kurulum

```bash
# Yüklemek
pip install pyHES

# Güncellemek
pip install -U pyHES
```

## 📝 Kullanım

### SMS Onayı İle Oturum Başlatma

```python
from pyHES import HES
from json import dumps

tokensiz_hes_sinifi = HES(telefon_numarasi = 5451112233)

giris = tokensiz_hes_sinifi.sms_gonder

if giris:
    veri = tokensiz_hes_sinifi.giris_dogrula(int(input("Lütfen SMS Kodunu Giriniz : ")))
    print(dumps(veri, indent=2, ensure_ascii=False, sort_keys=False))
```

### id_token ile İşlem Yapma

```python
from pyHES import HES

hes_sinifi = HES(
    telefon_numarasi = 5451112233,
    id_token         = "ASDQWEQWEQWEQWEASDASD"
)

print(hes_sinifi.bilgilerim())
print(hes_sinifi.hes_kodlarim())
print(hes_sinifi.hes_sorgula("A1B23456"))
```

### Çıktılar

```json
// .giris_dogrula(123456)
{
  "id_token": "ASDQWEQWEQWEQWEASDASD",
  "telefon": "+905451112233",
  "ad": "Ömer Faruk",
  "soyad": "Sancak",
  "cinsiyet": "Erkek",
  "dogum_tarihi": "07-10-1995",
  "durum": "Risksiz"
}
```

```json
// .bilgilerim()
{
  "id_token": "ASDQWEQWEQWEQWEASDASD",
  "telefon": "+905451112233",
  "ad": "Ömer Faruk",
  "soyad": "Sancak",
  "cinsiyet": "Erkek",
  "dogum_tarihi": "07-10-1995",
  "durum": "Risksiz",
  "hes_kodlarim": [
    {
      "hes_kodu": "A1B23456",
      "aciklama": "İstanbul Seyahati",
      "olusturma": "27-08-2020",
      "olusturan": "HES-EDEVLET",
      "gecerlilik": "27-02-2022"
    }
  ]
}
```

```json
// .hes_kodlarim()
[
  {
    "hes_kodu": "A1B23456",
    "aciklama": "İstanbul Seyahati",
    "olusturma": "27-08-2020",
    "olusturan": "HES-EDEVLET",
    "gecerlilik": "27-02-2022"
  }
]
```

```json
// .hes_sorgula("A1B23456")
{
  "hes_kodu": "A1B23456",
  "tc_kimlik_no": "********646",
  "ad": "ÖM**** FA****",
  "soyad": "SA**** ",
  "durum": "Risksiz",
  "gecerlilik": "27-02-2022"
}
```

## 🌐 Telif Hakkı ve Lisans

* *Copyright (C) 2021 by* [keyiflerolsun](https://github.com/keyiflerolsun) ❤️️
* [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](https://github.com/keyiflerolsun/pyHES/blob/main/LICENSE) *Koşullarına göre lisanslanmıştır..*

## ♻️ İletişim

*Benimle iletişime geçmek isterseniz, **Telegram**'dan mesaj göndermekten çekinmeyin;* [@keyiflerolsun](https://t.me/keyiflerolsun)

## 💸 Bağış Yap

**[☕️ Kahve Ismarla](https://KekikAkademi.org/Kahve)**

##

> **[@KekikAkademi](https://t.me/KekikAkademi)** *için yazılmıştır..*
