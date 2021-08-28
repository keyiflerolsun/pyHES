# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests import get, post
from requests.structures import CaseInsensitiveDict
import datetime

class HesKodu(object):
    """
    HesKodu : Cep Telefonu ile Giriş Yaparak HES Üretme, Listeleme, Sorgulama Yapabilirsiniz..

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
    def __repr__(self) -> str:
        return f"{__class__.__name__} Sınıfı -- {self.saglik_gov} ile haberleşmek için yazılmıştır.."

    def __init__(self, telefon_numarasi:int, id_token:None):
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
        dogum = datetime.datetime.strptime(veri['dob'],"%Y-%m-%d")
        return {
            # "kimlik_hash"   : veri['identityNumberHash'],
            # "id"            : veri['userId'],
            "id_token"      : veri['id_token'],
            # "refresh_token" : veri['refresh_token'],
            "telefon"       : f"+{veri['phone']}",
            "ad"            : veri['firstname'].title(),
            "soyad"         : veri['lastname'].title(),
            "cinsiyet"      : "Erkek" if veri['gender'] == "MALE" else "Kadın",
            "dogum_tarihi"  : dogum.strftime("%d-%m-%Y"),
            "durum"         : "Risksiz" if veri['healthStatus'] == "RISKLESS" else "Riskli",
        }

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
        dogum = datetime.datetime.strptime(veri['dob'],"%Y-%m-%d")
        return {
            # "kimlik_hash"   : veri['identityNumberHash'],
            # "id"            : veri['userId'],
            "id_token"      : self.id_token,
            # "refresh_token" : veri['refresh_token'],
            "telefon"       : f"+{veri['phone']}",
            "ad"            : veri['firstname'].title(),
            "soyad"         : veri['lastname'].title(),
            "cinsiyet"      : "Erkek" if veri['gender'] == "MALE" else "Kadın",
            "dogum_tarihi"  : dogum.strftime("%d-%m-%Y"),
            "durum"         : "Risksiz" if veri['healthStatus'] == "RISKLESS" else "Riskli",
        }


    def hes_sorgula(self, hes_kodu:str):
        "A1B23456 Şeklinde Hes Kodu Sorgulaması Yapılır. - id_token ile birlikte kullanılır!"
        if not self.id_token:
            return "Lütfen Sınıf İçerisinde id_token Bilgisi Giriniz!"

        hes = hes_kodu.replace('-', '').replace(' ', '')

        endpoint = "/services/hescodeproxy/api/check-hes-code"
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
        tarih = datetime.datetime.strptime(veri['expiration_date'],"%Y-%m-%dT%H:%M:%SZ")
        return {
            "hes_kodu"      : hes_kodu,
            "tc_kimlik_no"  : veri['masked_identity_number'],
            "ad"            : veri['masked_firstname'],
            "soyad"         : veri['masked_lastname'],
            "durum"         : "Risksiz" if veri['current_health_status'] == "RISKLESS" else "Riskli",
            "gecerlilik"    : tarih.strftime("%d-%m-%Y"), # "2021-12-31T00:00:00Z",
        }