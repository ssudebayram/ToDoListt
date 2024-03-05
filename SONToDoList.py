import json
from datetime import datetime
import uuid


class KullaniciDogrulama:
    def __init__(self):
        self.kullanici_adi = "ssudebayram"
        self.sifre = "sude1100"

    def giris_yap(self):
        while True:
            kullanici_adi = input("Kullanıcı adınızı giriniz: ")
            sifre = input("Şifrenizi giriniz: ")

            if kullanici_adi == self.kullanici_adi and sifre == self.sifre:
                print("Giriş başarılı.")
                return True
            else:
                print("Kullanıcı adı veya şifre yanlış. Tekrar deneyiniz.")



class AltSinif:

    def __init__(self, gorev_id , gorev_basligi, gorev_aciklamasi, son_tarih, gorev_son_durumu, olusturulma_tarihi=None):
        self.gorev_id = gorev_id
        self.gorev_basligi = gorev_basligi
        self.gorev_aciklamasi = gorev_aciklamasi
        self.son_tarih = son_tarih
        self.gorev_son_durumu = gorev_son_durumu
        self.olusturulma_tarihi=olusturulma_tarihi or datetime.now()




    def sozluge_donustur(self):

        return {
            "gorev_basligi": self.gorev_basligi,
            "gorev_aciklamasi": self.gorev_aciklamasi,
            "olusturulma_tarihi": self.olusturulma_tarihi.isoformat() if isinstance(self.olusturulma_tarihi, datetime) else self.olusturulma_tarihi,
            "son_tarih": self.son_tarih.isoformat() if isinstance(self.son_tarih, datetime) else self.son_tarih,
            "gorev_son_durumu": self.gorev_son_durumu
        }

class AnaSinif:

    def __init__(self, dosya_yolu):
        self.resultt_json = dosya_yolu
        self.gorevler = []
        self.gorevleri_yukle()
        self.kullanici_dogrulama = KullaniciDogrulama()

    def tarihi_gecmis_gorevleri_goster(self):
        tarihi_gecmis_gorevler = []
        for gorev in self.gorevler:
            son_tarih = gorev.son_tarih
            if isinstance(son_tarih, str):
                try:
                    son_tarih = datetime.strptime(son_tarih, "%d-%m-%Y")
                except ValueError:
                    son_tarih = datetime.fromisoformat(son_tarih)
            if son_tarih < datetime.now():
                tarihi_gecmis_gorevler.append(gorev)

        if tarihi_gecmis_gorevler:
            print("Tarihi Geçmiş Görevler:")
            for indeks, gorev in enumerate(tarihi_gecmis_gorevler, start=1):
                print(f"{indeks}. Başlık: {gorev.gorev_basligi}, Son Tarih: {gorev.son_tarih}")
        else:
            print("Tarihi geçmiş görev bulunamadı.")





    def tarihi_gecmis_gorevleri_sil(self):
        self.tarihi_gecmis_gorevleri_goster()
        silme_secimi = input("Tarihi geçmiş görevleri silmek istiyor musunuz? (evet/hayır): ")
        if silme_secimi.lower() == "evet":
            yeni_gorevler = []
            for gorev in self.gorevler:
                if isinstance(gorev.son_tarih, str):
                    try:
                        son_tarih = datetime.strptime(gorev.son_tarih, "%d-%m-%Y")
                    except ValueError:
                        son_tarih = datetime.fromisoformat(gorev.son_tarih)
                else:
                    son_tarih = gorev.son_tarih

                if son_tarih >= datetime.now():
                    yeni_gorevler.append(gorev)

            self.gorevler = yeni_gorevler
            self.gorevleri_kaydet()
            print("Tarihi geçmiş görevler silindi.")
        else:
            print("Silme işlemi iptal edildi.")



    def gorevleri_yukle(self):
        try:
            with open(self.resultt_json, 'r') as f:
                data = f.read()
                if data.strip():
                    self.gorevler = [AltSinif(gorev_id = None , **gorev) for gorev in json.loads(data)]
        except FileNotFoundError:
            print("Dosya bulunamadı.")
        except json.decoder.JSONDecodeError:
            print("JSON verisi yüklenirken hata oluştu. Dosya geçersiz bir JSON formatına sahip olabilir.")

            self.gorevleri_yukle()

    def gorevleri_kaydet(self):
        try:
            mevcut_gorevler = [gorev.sozluge_donustur() for gorev in self.gorevler]

            with open(self.resultt_json, 'w') as dosya:
                json.dump(mevcut_gorevler, dosya, indent=4)

            print("Görevler başarıyla kaydedildi.")
        except Exception as e:
            print("Hata:", e)
        


    def gorev_ekle(self):
        gorev_basligi = input("Görev başlığını giriniz: ")


        for gorev in self.gorevler:
            if gorev.gorev_basligi == gorev_basligi:
                print("Bu başlıkta bir görev zaten var. Yeni görev eklenemedi.")
                return

        gorev_aciklamasi = input("Görev açıklamasını giriniz: ")
        try:
            print("Görevin son tarihini D-M-Y formatında giriniz.")
            son_tarih_str = input("Görevin son tarihini giriniz: ")
            son_tarih = datetime.strptime(son_tarih_str, "%d-%m-%Y")
        except ValueError:
            print("Geçersiz tarih formatı. Lütfen tarihi D-M-Y formatında giriniz.")
            return
        gorev_son_durumu = input("Görevin son durumunu giriniz: ")

        yeni_gorev = AltSinif(None ,gorev_basligi, gorev_aciklamasi, son_tarih, gorev_son_durumu)

        self.gorevler.append(yeni_gorev)
        self.gorevleri_kaydet()
        print("Görev eklendi.")

    def gorev_sil(self):
        baslik = input("Silinecek görevin başlığını giriniz: ")
        silindi = False
        for gorev in self.gorevler:
            if gorev.gorev_basligi == baslik:
                self.gorevler.remove(gorev)
                self.gorevleri_kaydet()
                print("Görev silindi.")
                silindi = True
                break
        if not silindi:
            print("Görev bulunamadı.")

    def gorev_guncelle(self):
        baslik = input("Güncellenecek görev başlığını giriniz: ")
        for indeks , gorev in enumerate(self.gorevler):
            if gorev.gorev_basligi == baslik:
                self.gorevler[indeks].gorev_basligi = input("Yeni görev başlığını giriniz: ")
                self.gorevler[indeks].gorev_aciklamasi = input("Yeni görev açıklamasını giriniz: ")
                try:
                    son_tarih_str = input("Görevin yeni son tarihini giriniz: ")
                    self.gorevler[indeks].son_tarih = datetime.strptime(son_tarih_str, "%d-%m-%Y")
                except ValueError:
                    print("Geçersiz tarih formatı. Lütfen tarihi D-M-Y formatında giriniz.")
                    return

                self.gorevler[indeks].gorev_son_durumu = input("Görevin yeni son durumunu giriniz: ")


                self.gorevleri_kaydet()
                print("Görev güncellendi.")
                break
        else:
            print("Görev bulunamadı.")

    def gorevleri_listele(self):
        try:
            with open(self.resultt_json, 'r') as f:
                data = f.read()
                if data.strip():
                    gorevler = json.loads(data)
                    filtre_basligi = input("Listelemek istediğiniz görev başlığını giriniz , boş bırakılması halinde tüm görevler listelenir")
                    for indeks, gorev_dict in enumerate(gorevler, start=1):
                        gorev = AltSinif(gorev_id = None , **gorev_dict)
                        if not filtre_basligi or gorev.gorev_basligi ==filtre_basligi:
                            print(f"Başlık: {gorev.gorev_basligi}")
                            print(f"Açıklama: {gorev.gorev_aciklamasi}")
                            print(f"Son Teslim Tarihi: {gorev.son_tarih}")
                            print(f"Görev oluşturulma tarihi: {gorev.olusturulma_tarihi}")
                            print(f"Durum: {gorev.gorev_son_durumu}")

        except FileNotFoundError:
            print("Dosya bulunamadı.")
        except json.decoder.JSONDecodeError:
            print("JSON verisi yüklenirken hata oluştu. Dosya geçersiz bir JSON formatına sahip olabilir.")

    def gorevleri_sil(self):
        silme_onay = input("Tüm görevleri silmek istediğinizden emin misiniz? (evet/hayır): ")
        if silme_onay.lower() == "evet":
            self.gorevler = []
            self.gorevleri_kaydet()
            print("Tüm görevler silindi.")
        else:
            print("Silme işlemi iptal edildi.")


    def ana_menu(self):
            if self.kullanici_dogrulama.giris_yap():
                while True:
                    print("1-Görev Ekle")
                    print("2-Görev Sil")
                    print("3-Görev Güncelle")
                    print("4-Görevleri Listele")
                    print("5-Tarihi geçmiş görevleri listele")
                    print("6-Tüm görevleri sil")
                    secim = input("Yapmak istediğiniz işlemi seçiniz (1/2/3/4/5/6): ")
                    if secim == "1":
                        self.gorev_ekle()
                    elif secim == "2":
                        self.gorev_sil()
                    elif secim == "3":
                        self.gorev_guncelle()
                    elif secim == "4":
                        self.gorevleri_listele()
                    elif secim == "5":
                        self.tarihi_gecmis_gorevleri_sil()
                    elif secim == "6":
                        self.gorevleri_sil()
                    else:
                        print("Geçersiz seçim. Lütfen geçerli bir seçim yapınız.")

if __name__ == "__main__":
  json_dosya_yolu = "resultt_json"
  ana_sinif = AnaSinif(json_dosya_yolu)
  ana_sinif.ana_menu()






