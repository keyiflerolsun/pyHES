# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests import get, post
from requests.structures import CaseInsensitiveDict
import datetime
from pyzbar import pyzbar
from PIL import Image

class HES(object):
    """
    HES : Cep Telefonu ile Giriş Yaparak HES Üretme, Listeleme, Sorgulama Yapabilirsiniz..

    Methodlar
    ----------
        .sms_gonder:
            Hayat Eve Sığar Uygulamasın'a Giriş Kodunu SMS ile Cep Telefon Numaranıza Atar.
        .giris_dogrula(giris_kodu:int):
            oturum ve kişi bilgilerini döndürür.
        .bilgilerim():
            Kişi Bilgilerini döndürür - id_token ile birlikte kullanılır!
        .hes_sorgula(hes_kodu:str):
            A1B23456 Şeklinde Hes Kodu Sorgulaması Yapılır. - id_token ile birlikte kullanılır!
    """

    tarih_cevir = lambda tarih: datetime.datetime.strptime(tarih.split('T')[0],"%Y-%m-%d").strftime("%d-%m-%Y")

    def __repr__(self) -> str:
        return f"{__class__.__name__} Sınıfı -- {self.saglik_gov} ile haberleşmek için yazılmıştır.."

    def __init__(self, telefon_numarasi:int, id_token:str=None):
        "telefon numaranız 5 ile başlamalıdır.."
        self.saglik_gov = "https://hessvc.saglik.gov.tr"
        self.telefon_numarasi = telefon_numarasi
        self.id_token = id_token

        if id_token:
            self.yetki = CaseInsensitiveDict()
            self.yetki["Content-Type"]  = "application/json"
            self.yetki["Authorization"] = f"Bearer {id_token}"

    @property
    def sms_gonder(self) -> bool:
        "Doğrulama Kodunu Telefona Sms Gönderir"
        endpoint = "/api/send-code-to-login"
        istek    = post(
            f"{self.saglik_gov}{endpoint}",
            json = {
                "phone": f"+90{self.telefon_numarasi}"
            }
        )
        return istek.status_code == 201

    def giris_dogrula(self, giris_kodu:int):
        "Giriş Kodu İle Oturum Başlatır"
        endpoint = "/api/authenticate-with-code"
        istek    = post(
            f"{self.saglik_gov}{endpoint}",
            json = {
                "password"  : f"{giris_kodu}",
                "phone"     : f"+90{self.telefon_numarasi}",
                "rememberMe": True
            }
        )
        if istek.status_code != 200:
            return False

        veri  = istek.json()
        return {
            # "kimlik_hash"   : veri['identityNumberHash'],
            # "id"            : veri['userId'],
            "id_token"      : veri['id_token'],
            # "refresh_token" : veri['refresh_token'],
            "telefon"       : f"+{veri['phone']}",
            "ad"            : veri['firstname'].title(),
            "soyad"         : veri['lastname'].title(),
            "cinsiyet"      : "Erkek" if veri['gender'] == "MALE" else "Kadın",
            "dogum_tarihi"  : HES.tarih_cevir(veri['dob']),
            "durum"         : "Risksiz" if veri['healthStatus'] == "RISKLESS" else "Riskli"
        }

    def hes_kodlarim(self):
        "Hes Kodlarını döndürür - id_token ile birlikte kullanılır!"
        if not self.id_token:
            return "Lütfen Sınıf İçerisinde id_token Bilgisi Giriniz!"

        endpoint = "/services/hescodeproxy/api/hes-codes"
        istek    = post(
            f"{self.saglik_gov}{endpoint}",
            headers = self.yetki
        )

        if istek.status_code != 200:
            return False

        veriler = istek.json()
        return [
            {
                "hes_kodu"   : veri['hes_code'],
                "aciklama"   : veri['description'],
                "olusturma"  : HES.tarih_cevir(veri['created_date']),
                "olusturan"  : veri['created_by'].upper(),
                "gecerlilik" : HES.tarih_cevir(veri['expiration_date'])
            }
            for veri in veriler
        ]

    def bilgilerim(self):
        "Kişi Bilgilerini döndürür - id_token ile birlikte kullanılır!"
        if not self.id_token:
            return "Lütfen Sınıf İçerisinde id_token Bilgisi Giriniz!"

        endpoint = "/api/account-with-token"
        istek    = get(
            f"{self.saglik_gov}{endpoint}",
            headers = self.yetki
        )

        if istek.status_code != 200:
            return False

        veri  = istek.json()
        return {
            # "kimlik_hash"   : veri['identityNumberHash'],
            # "id"            : veri['userId'],
            "id_token"      : self.id_token,
            # "refresh_token" : veri['refresh_token'],
            "telefon"       : f"+{veri['phone']}",
            "ad"            : veri['firstname'].title(),
            "soyad"         : veri['lastname'].title(),
            "cinsiyet"      : "Erkek" if veri['gender'] == "MALE" else "Kadın",
            "dogum_tarihi"  : HES.tarih_cevir(veri['dob']),
            "durum"         : "Risksiz" if veri['healthStatus'] == "RISKLESS" else "Riskli",
            "hes_kodlarim"  : self.hes_kodlarim()
        }


    def hes_sorgula(self, hes_kodu:str):
        "A1B23456 Şeklinde Hes Kodu Sorgulaması Yapılır. - id_token ile birlikte kullanılır!"
        if not self.id_token:
            return "Lütfen Sınıf İçerisinde id_token Bilgisi Giriniz!"

        hes = hes_kodu.replace('-', '').replace(' ', '')

        endpoint = "/services/hescodeproxy/api/check-hes-code-plus"
        istek = post(
            f"{self.saglik_gov}{endpoint}",
            headers = self.yetki,
            json = {
                "hes_code"  : hes,
            }
        )

        if istek.status_code != 200:
            return False

        veri  = istek.json()
        return {
            "hes_kodu"       : hes_kodu,
            "tc_kimlik_no"   : veri['masked_identity_number'],
            "ad"             : veri['masked_firstname'],
            "soyad"          : veri['masked_lastname'],
            "durum"          : "Risksiz" if veri['current_health_status'] == "RISKLESS" else "Riskli",
            "asi"            : veri['is_vaccinated'],
            "bagisiklik"     : veri['is_immune'],
            "test"           : veri['is_tested'],
            "uygunluk"       : veri['is_eligible'],
            "uygunluk_metin" : veri['eligible_text'],
            "gecerlilik"     : HES.tarih_cevir(veri['expiration_date'])
        }
    
    def qr_sorgula(self, image_path:str):
        qr = pyzbar.decode(Image.open(image_path))
        return self.hes_sorgula(qr[0].data.decode("utf8").split("|")[-1])
