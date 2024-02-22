
from PyQt5 import QtCore, QtWidgets , QtGui 
import pygame
from PyQt5.QtCore import QThread,pyqtSignal,QTimer
import sys
from PyQt5.QtGui import QCloseEvent, QPaintEvent
from rehberpencere import Ui_FORM               
from statstasarim import Ui_MainWindow          
import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import urllib
import urllib3


if getattr(sys,'frozen', False):
    exe_is_running = True             
    os.chdir(sys._MEIPASS)
  
    os.chdir('..')         
    klasor_var = []
    klasor_kontrol = os.listdir(os.getcwd())
    for i in klasor_kontrol:
        if i == 'LOL Bilgileri':
            klasor_var.append(i)
    try:
        if klasor_var[0] == 'LOL Bilgileri':
            pass
    except IndexError:
        os.mkdir('LOL Bilgileri')   
    os.chdir(sys._MEIPASS) 
     
else:
    exe_is_running = False
    os.chdir('.')



class info_update(QThread):
    def __init__(self,stats_instance):
        super(info_update,self).__init__()
        self.infoupdate = stats_instance
        self.islemler_bitti.connect(self.eskiyedondur)
        self.islem_devam = True
        self.guncelleme_devam = True
    islemler_bitti = pyqtSignal()                
    signal_veri_yazildi = pyqtSignal()
    signal_veri_guncelleme_tamamlandi = pyqtSignal()
    signal_veri_guncelleme_basarisiz = pyqtSignal()
    def run(self):
        try:
            for i in self.infoupdate.champions:
                url = 'https://leagueoflegends.fandom.com/wiki/'+i+'/LoL'
                html = requests.get(url)
                soup = BeautifulSoup(html.content,'html.parser') 
                ozet = soup.find_all('aside',{'role':'region'})
                if exe_is_running is True:
                    os.chdir('..') 
                    with open('LOL Bilgileri\\'+i+'.py','w', encoding='UTF-8') as file:
                        file.write(str(ozet))   
                        os.chdir(sys._MEIPASS)        
                    self.signal_veri_yazildi.emit()
                    if self.guncelleme_devam is False:
                        break 
                elif exe_is_running is False:
                    with open('bilgiler\\'+i+'.py','w', encoding='UTF-8') as file:
                        file.write(str(ozet))            
                    self.signal_veri_yazildi.emit()
                    if self.guncelleme_devam is False:
                        break
            self.signal_veri_guncelleme_tamamlandi.emit()

        except requests.exceptions.ConnectionError:
            self.signal_veri_guncelleme_basarisiz.emit()

        self.islemler_bitti.emit() 

    def guncelleme(self):
        self.guncelleme_devam = False
    def durdur(self):
        self.islem_devam = False
    def eskiyedondur(self):
        self.islem_devam = True  


class rehber(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui_win2 = Ui_FORM()
        self.ui_win2.setupUi(self)
        simge_lol = QtGui.QPixmap('image\\icon\\lol.png')
        self.setWindowIcon(QtGui.QIcon(simge_lol))
        self.setFixedSize(self.width(),self.height())
    signal_rehber_kapama_islemleri = pyqtSignal()
    def TR_REH(self):
        self.setWindowTitle('REHBER')
        self.ui_win2.label_rehber_mod.setText('Diğer oyun modu istatistikleri -->  Kapalı - Açık')
        self.ui_win2.label_rehber_cevrimdisi.setText('Çevrimiçi veri kullanımı  -->  Kapalı - Açık')
        self.ui_win2.label_rehber_aciklama_cevrimici.setText('Çevrimdışı Modu : Verileri bir kez güncelledikten sonra bu modu kullanmak uygulamanın veri\nanalizi yaparkenki hızını büyük ölçüde arttırır fakat daha önce kaydedilen\nveriyi göstereceği için gelen yama istatistiklerini yansıtmayabilir.\nÇevrimiçi Modu : Sürekli güncel bilgilere erişim sağlar ama verilerin işlenmesi sırasında birkaç \nsaniyelik gecikmeler yaşanabilir.')
        self.ui_win2.label_rehber_bilgi.setText('Bilgilendirme  -->  Kapalı - Açık')
        self.ui_win2.label_rehber_ayarlar.setText('Ayarlar  -->  Kapalı - Açık - Güncelleniyor')
        self.ui_win2.label_rehber_guncelleme.setText('Veri güncelleme durumu  -->  Kapalı - Açık - Güncelleniyor')
        self.ui_win2.label_rehber_aciklama_guncelleme.setText('Güncelleme sırasında veri yedeklemenin hangi durumda olduğunu görmek için ayarlar\nsekmesinin altındaki güncelleme çubuğu takip edilebilir.Ayarlar ve güncelleme butonunun\nsimgesinin maviye dönmesi veri güncellemesi yaptığının kullanıcıya bildirilmesi anlamına gelir.\nGüncellemeyi uygulamanın her açılışında otomatik olarak yapması için Otomatik Güncelle\nseçeneğini seçebilir, ya da bunu devre dışı bırakarak istediğiniz zaman güncellemek yapmak için\nManuel Güncelle Butonunu kullanabilirsiniz')
        self.ui_win2.label_rehber_champses.setText('Şampiyon seçim sesleri  -->  Kapalı - Açık')
        self.ui_win2.label_rehber_kaynak.setText('Veriler; https://leagueoflegends.fandom.com adresinden alınmaktadır.')
        self.ui_win2.label_rehber_arama.setText('Şampiyon arama  -->  Kapalı - Açık')
    def EN_REH(self):
        self.setWindowTitle('GUIDE')
        self.ui_win2.label_rehber_mod.setText('Other game mode statistics  -->  Off - On')
        self.ui_win2.label_rehber_cevrimdisi.setText('Online data usage  -->  Off - On')
        self.ui_win2.label_rehber_aciklama_cevrimici.setText('Offline Mode: After updating the data once, using this mode greatly increases the speed of\nthe application when analyzing data, but it may not reflect the incoming patch\nstatistics as it will show previously saved data.\nOnline Mode: Provides access to constantly updated information, but there may be a\ndelay of a few seconds during the processing of the data.')
        self.ui_win2.label_rehber_bilgi.setText('Information  -->  Off - On')
        self.ui_win2.label_rehber_ayarlar.setText('Settings  -->  Off - On - Updating')
        self.ui_win2.label_rehber_guncelleme.setText('Data update status  -->  Off - On - Updating')
        self.ui_win2.label_rehber_aciklama_guncelleme.setText('You can follow the update bar under the settings tab to see the data backup status\nduring the update. When the settings and update button icon turns blue, the user is\ninformed that their data has been updated. You can select or disable the Auto Update option to have\nthe app automatically update every time it is opened.\nYou can use the Manual Update Button to update whenever you want.')
        self.ui_win2.label_rehber_champses.setText('Champion selection sounds  -->  Off - On')
        self.ui_win2.label_rehber_kaynak.setText('Datas; Retrieved from https://leagueoflegends.fandom.com')
        self.ui_win2.label_rehber_arama.setText('Champion search  -->  Off - On')

    def closeEvent(self,event):
        self.signal_rehber_kapama_islemleri.emit()
        

class Stats(QtWidgets.QMainWindow):
    def __init__(self):
        super(Stats,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mod_kapali = True
        self.ayarlar_kapali = True
        self.ilerleme_durumu_kapali = True
        self.campses_acik = True
        self.cevrimdisimod = False
        self.bilgi_acik = False
        self.islem_devam = False
        self.arama_champ = False
        self.ilerlemedurumu_proggres = 0     

    
        self.internet_yok = QtWidgets.QMessageBox()
        self.simge_kapat = QtGui.QPixmap('image\\icon\\close.png')
        self.simge_bilgi = QtGui.QPixmap('image\\icon\\bilgi.png')
        self.simge_internet = QtGui.QPixmap('image\\icon\\internet.png')
        self.simge_yenile = QtGui.QPixmap('image\\icon\\yenile.png')
        self.simge_cevrimdisi= QtGui.QPixmap('image\\icon\\cevrimdisi.png')
        self.simge_tamam = QtGui.QPixmap('image\\icon\\ok.png')
        self.simge_guncelle = QtGui.QPixmap('image\\icon\\update.png')
        self.simge_lolsimge = QtGui.QPixmap('image\\icon\\lol_simge.png')
        self.simge_lolicon = QtGui.QPixmap('image\\icon\\lol.png')
        self.simge_rehber = QtGui.QPixmap('image\\icon\\rehber.png')
        self.internet_yok.setStyleSheet('color:white ; background-color:black')
      

        self.win2 = rehber()      
        self.update_thread = info_update(self)

        self.setWindowTitle('LOL Bilgileri')
        
        self.modcerceve = self.ui.frame_mod.width()          
        self.ayarcerceve = self.ui.frame_ayarlar.height()
        self.ilk_boyut_olcu_yatay = QtWidgets.QMainWindow.width(self)          
        self.ilk_boyut_olcu_dikey = QtWidgets.QMainWindow.height(self)
        self.son_boyut_olcu_yatay = self.width() - self.modcerceve - 20
        self.son_boyut_olcu_dikey = self.height() - self.ayarcerceve - 5
        self.setFixedSize(self.son_boyut_olcu_yatay, self.son_boyut_olcu_dikey )     

        self.ilk_scroll_olcu_dikey = self.ui.scrollArea_camp.height()           
        self.son_scroll_olcu_dikey = self.ui.scrollArea_camp.height() + 47
        if self.arama_champ is False:           
            self.ui.lineEdit_samp_arama.hide()
            self.ui.scrollArea_camp.setFixedHeight(self.son_scroll_olcu_dikey)

        simge_lol = QtGui.QPixmap('image\\icon\\lol.png')
        
        self.setWindowIcon(QtGui.QIcon(simge_lol))
        
        self.kullanici_secimlerini_yukle()
        self.camp_name_btn()       
        self.deger_hizala()        
        
        #buton komutları
        self.ui.buton_modlar.clicked.connect(self.modlari_ac_kapat)
        self.ui.buton_ayarlar.clicked.connect(self.ayarlari_ac_kapat)
        self.ui.buton_guncelle.clicked.connect(self.manuel_guncelle)
        self.ui.buton_yuklemedurumu.clicked.connect(self.ilerlemeyi_ac_kapat)
        self.ui.buton_sescamp.clicked.connect(self.camp_ses_ac_kapat)
        self.ui.buton_cevrimdisi.clicked.connect(self.cevrimdisimod_ac_kapat)
        self.ui.buton_bilgi.clicked.connect(self.bilgi_ac_kapat)
        self.ui.buton_samp_arama.clicked.connect(self.camp_arama_ac_kapat)

        #thread sinyalleri
        self.update_thread.signal_veri_yazildi.connect(self.veri_durum)
        self.update_thread.signal_veri_guncelleme_tamamlandi.connect(self.progresi_sifirla)
        self.update_thread.signal_veri_guncelleme_basarisiz.connect(self.veri_guncelleme_basarisiz)
        #diğer sinyaller
        self.win2.signal_rehber_kapama_islemleri.connect(self.rehber_kapat)         
        
        vlayoutscrollarea = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)        
        
        self.ui.lineEdit_samp_arama.textChanged.connect(self.sampiyon_arama_cubugu)   

        

        for a in self.champions:                                                        
            buttonn = QtWidgets.QPushButton(a,self)
            buttonn.setIcon(QtGui.QIcon('image\\sampiyonlar\\'+a+'.png'))
            buttonn.setIconSize(QtCore.QSize(30,30))
            vlayoutscrollarea.addWidget(buttonn)
            buttonn.clicked.connect(self.button_func)  
        
        
    '''def paintEvent(self,event):                      #resmin pencereye göre ölçeklendirilmesi için
        image_background = QtGui.QPixmap('image\\arkaplan\\6.jpg')
        ekran_olcu = self.size()
        background_image = image_background.scaled(ekran_olcu,aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(),background_image) '''   

    def sampiyon_arama_cubugu(self):
        butonlar_champ = self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QPushButton)
        aranan = self.ui.lineEdit_samp_arama.text()
        for i in butonlar_champ:
            if  aranan.lower() in i.text().lower():
                i.show()
            else:
                i.hide()

    def button_func(self):
        self.okunabilir_veri = True
        senderbutton = self.sender()
        name = senderbutton.text()
                 
        
        for i in self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QPushButton):
            if i == senderbutton:
                ses_seviyesi = self.ui.slider_campsound.value()/100
                i.setStyleSheet('border-style: outset;border-width: 0px;border-radius: 10px;border-color: rgb(136, 136, 68) ; text-align: center ; font: 57 10pt "Dubai Medium"; background-color: qconicalgradient(cx:0.5, cy:0.5, angle:50, stop:0 rgba(101, 181, 192, 255), stop:0.16 rgba(70, 199, 217, 255), stop:0.225 rgba(41, 150, 166, 255), stop:0.285 rgba(74, 188, 204, 255), stop:0.345 rgba(102, 218, 235, 255), stop:0.415 rgba(112, 228, 245, 255), stop:0.52 rgba(76, 192, 209, 255), stop:0.57 rgba(51, 170, 187, 255), stop:0.632184 rgba(52, 195, 215, 255), stop:0.695 rgba(68, 185, 202, 255), stop:0.75 rgba(86, 202, 218, 255), stop:0.815 rgba(73, 191, 208, 255), stop:0.88 rgba(88, 220, 239, 255), stop:0.935 rgba(71, 205, 224, 255), stop:1 rgba(67, 193, 211, 255));')            
                if self.campses_acik is True and ses_seviyesi != 0:
                    if exe_is_running is True:
                        os.chdir(sys._MEIPASS)          
                    pygame.mixer.init()
                    try:
                        pygame.mixer_music.load('sound\\'+name+'.ogg')          
                    except pygame.error:
                        self.internet_yok.setIconPixmap(self.simge_bilgi)
                        self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_kapat))
                        self.internet_yok.setStandardButtons(QtWidgets.QMessageBox.Ok )
                        butonok = self.internet_yok.button(QtWidgets.QMessageBox.Ok)
                        butonok.setIcon(QtGui.QIcon(self.simge_tamam))
                        if self.ui.radioButton_tr.isChecked():
                            butonok.setText('TAMAM')       
                            self.internet_yok.setWindowTitle('SES DOSYASI BULUNAMADI !')
                            self.internet_yok.setText('\n\n\nSeçilen şampiyona ait ses\ndosyası bulunamadı.')
                        elif self.ui.radioButton_en.isChecked():
                            butonok.setText('OK')       
                            self.internet_yok.setWindowTitle('SOUND FILE NOT FOUND !')
                            self.internet_yok.setText('\n\n\nNo audio file for the\nselected champion was found.')
                        x = self.internet_yok.exec_()
                        if x == QtWidgets.QMessageBox.Ok:
                            pass 
                    pygame.mixer_music.set_volume(ses_seviyesi)
                    pygame.mixer_music.play()
                elif self.campses_acik is False:
                    pass
            if i != senderbutton:
                i.setStyleSheet('initial')
    
        self.can_bilgi = []
        self.mana_bilgi = []
        self.can_yenilenmesi = []
        self.mana_yenilenmesi = []
        self.zirh = []
        self.saldiri_gücü = []
        self.buyu_direnci = []
        self.kritik_sansi = []
        self.hareket_hizi = []
        self.saldiri_menzili = []
        self.temel_saldiri_hizi = []
        self.saldiri_sonlandirma = []
        self.saldiri_hizi_orani = []
        self.bonus_saldiri_hizi = []
        self.oyun_yaricap = []
        self.secim_yaricap = []
        self.yol_yaricap = []
        self.edinme_yaricap = []

        self.aram = []
        self.nexus_blitz = []
        self.birimiz_hepimiz_icin = []
        self.urf = []
        self.ulti_buyu_kitabi = []
        self.arena = []
    
        
        
        
        
        
        if self.cevrimdisimod is False:
            try:
                url = 'https://leagueoflegends.fandom.com/wiki/'+name+'/LoL'
                html = requests.get(url).content 
                self.okunabilir_veri = True  
                if requests.get(url).status_code != 200:        
                    '''html = urllib.request.urlopen(url)           #yukardaki kütüphane 200 kodu vermezse başka kütüphaneyi deniycek
                    if urllib.request.urlopen(url).code != 200:         #aynı şekilde
                        http = urllib3.PoolManager()                        #başka kütüphanelere yönlendirme devredışı bırakıldı sonuçta hepsi 200 kodu ile işlem yapıyor. kütüphane çalışmazsa diğerlerini dene unutma.
                        html = http.request('GET',url).data
                        if http.request('GET',url).status != 200:           #bu kütüphanede yanıt alamazsa kayıtlı verilere yönlendiricek.
                            #site erişimi reddedince yukardaki öğeleri bulamıyor. kayıtlı verilere yönlendirme'''
                    self.ui.buton_guncelle.setDisabled(True)        
                    self.ui.checkBox_otomatikguncelle.setChecked(False)
                    self.ui.checkBox_otomatikguncelle.setDisabled(True)
                    if exe_is_running is True:
                        os.chdir('..') 
                        with open('LOL Bilgileri\\'+name+'.py','r', encoding='UTF-8') as file:    
                            html = file.read()
                            soup = BeautifulSoup(html,'html.parser')
                            os.chdir(sys._MEIPASS) 
                    elif exe_is_running is False:
                        with open('bilgiler\\'+name+'.py','r', encoding='UTF-8') as file:     
                            html = file.read()
            except requests.exceptions.ConnectionError  :
                self.internet_yok.setIconPixmap(self.simge_bilgi)
                self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_internet))
                self.internet_yok.setStandardButtons( QtWidgets.QMessageBox.Close  |  QtWidgets.QMessageBox.Open )
                butonclose = self.internet_yok.button(QtWidgets.QMessageBox.Close) 
                butonclose.setIcon(QtGui.QIcon(self.simge_kapat))
                butonopen = self.internet_yok.button(QtWidgets.QMessageBox.Open) 
                butonopen.setIcon(QtGui.QIcon(self.simge_cevrimdisi))
                if self.ui.radioButton_tr.isChecked():
                    self.internet_yok.setWindowTitle('BAĞLANTI YOK !')
                    self.internet_yok.setText('\n\nİnternet bağlantınız kesilmiş\ngibi görünüyor.Bağlantınız tekrar kurulana\nkadar önceden kaydettiğiniz verilerle\nçevrimdışı modumuzu kullanmak istermisiniz ?')
                    butonclose.setText('KAPAT')
                    butonopen.setText('ÇEVRİMDIŞI MOD')
                elif self.ui.radioButton_en.isChecked():
                    self.internet_yok.setWindowTitle('NO CONNECTION !')
                    self.internet_yok.setText('\nIt looks like your internet connection\nhas been disconnected. Would\nyou like to use our offline mode\nwith your previously saved data until\nyour connection is re-established?')
                    butonclose.setText('CLOSE')
                    butonopen.setText('OFFLINE MODE')
            
                x = self.internet_yok.exec_()
                if x == QtWidgets.QMessageBox.Open:
                    
                    if self.cevrimdisimod is False:
                        self.ui.buton_cevrimdisi.click()        
                    self.okunabilir_veri = True         
                elif x == QtWidgets.QMessageBox.Close:
                    self.baglanti_yok = False
                    self.okunabilir_veri = False
                    self.close()      
        if self.cevrimdisimod is True:         
            try:
                if exe_is_running is True:
                    os.chdir('..') 
                    with open('LOL Bilgileri\\'+name+'.py','r', encoding='UTF-8') as file:       
                        html = file.read()
                        os.chdir(sys._MEIPASS) 
                elif exe_is_running is False:
                    with open('bilgiler\\'+name+'.py','r', encoding='UTF-8') as file:       
                        html = file.read()
                self.okunabilir_veri = True
            except FileNotFoundError:         
                self.okunabilir_veri = False
                self.internet_yok.setIconPixmap(self.simge_bilgi)
                self.internet_yok.setStandardButtons( QtWidgets.QMessageBox.Close  |  QtWidgets.QMessageBox.Open )
                butonclose = self.internet_yok.button(QtWidgets.QMessageBox.Close) 
                butonclose.setIcon(QtGui.QIcon(self.simge_kapat))
                butonopen = self.internet_yok.button(QtWidgets.QMessageBox.Open) 
                self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_lolsimge))
                butonopen.setIcon(QtGui.QIcon(self.simge_tamam))
                if self.ui.radioButton_tr.isChecked():
                    self.internet_yok.setWindowTitle('ŞAMPİYONA AİT KAYITLI VERİ BULUNAMADI !')
                    self.internet_yok.setText('Çevrimdışı modu kullanabilmek için en az\nbir kere verileri güncellemeniz gerekir.\nVerileri bilgisayarınızda bulamadığımız için\nçevrimdışı modu kullanılamıyor.\nLütfen internet bağlantınızı sağladığınızda\nisterseniz manuel olarak güncelleme,\nveya her uygulama açıldığında otomatik\ngüncelleme opsiyonlarından birini seçerek\nçevrimdışı modunda kullanacağınız\nverileri yedekleyebilirsiniz.')
                    butonclose.setText('KAPAT')
                    butonopen.setText('TAMAM')
                elif self.ui.radioButton_en.isChecked():
                    self.internet_yok.setWindowTitle('NO RECORDED DATA FOUND FOR THE CHAMPION !')
                    self.internet_yok.setText('To use offline mode, you need to update the\ndata at least once. Since we cannot find\nthe data on your computer, offline mode\ncannot be used. Please back up the\ndata you will use in offline mode by selecting\none of the options of manually updating\nwhen you have an internet connection\nor automatic update every time\nthe application is opened.')
                    butonclose.setText('CLOSE')
                    butonopen.setText('OK')
                x = self.internet_yok.exec_()
                if x == QtWidgets.QMessageBox.Open:
                    if exe_is_running is True:
                        os.chdir(sys._MEIPASS)
                    elif exe_is_running is False:
                        os.chdir('.')

                elif x == QtWidgets.QMessageBox.Close:
                    self.baglanti_yok = False
                    self.close()

        
        
    
        if self.okunabilir_veri is True : 
            soup = BeautifulSoup(html,'html.parser') 
            self.baglanti_aktif = True
            health = soup.find('div',{'data-source':'health'})          
            health_value = health.find_all('span')
            for i in health_value:
                if i.text:
                    self.can_bilgi.append((i.text))
            self.can_bilgi = "  ".join(self.can_bilgi)
            
                    

            mana = soup.find('div',{'data-source':'resource'}).find_next('div',{'data-source':'resource'})      
            mana_value = mana.find_all('span')
            for i in mana_value:
                if i.text:
                    self.mana_bilgi.append((i.text))
            self.mana_bilgi = "  ".join(self.mana_bilgi)
            self.mana_bilgi = self.mana_bilgi.replace('Energy','Enerji')


            health_reg = soup.find('div',{'data-source':'health regen'})
            health_reg_value = health_reg.find_all('span')
            for i in health_reg_value:
                if i.text:
                    self.can_yenilenmesi.append((i.text))
            self.can_yenilenmesi = "  ".join(self.can_yenilenmesi)


            mana_reg = soup.find('div',{'data-source':'resource regen'})
            mana_reg_value = mana_reg.find_all('span')
            for i in mana_reg_value:
                if i.text:
                    self.mana_yenilenmesi.append((i.text))
            self.mana_yenilenmesi = "  ".join(self.mana_yenilenmesi)



            armor = soup.find('div',{'data-source':'armor'})
            armor_value = armor.find_all('span')
            for i in armor_value:
                if i.text:
                    self.zirh.append((i.text))
            self.zirh = "  ".join(self.zirh)



            attack_damage = soup.find('div',{'data-source':'attack damage'})
            attack_damage_value = attack_damage.find_all('span')
            for i in attack_damage_value:
                if i.text:
                    self.saldiri_gücü.append((i.text))
            self.saldiri_gücü = "  ".join(self.saldiri_gücü)


            magic_resist = soup.find('div',{'data-source':'mr'})
            magic_resist_value = magic_resist.find_all('span')
            for i in magic_resist_value:
                if i.text:
                    self.buyu_direnci.append((i.text))
            self.buyu_direnci = "  ".join(self.buyu_direnci)



            crit_damage = soup.find('div',{'data-source':'critical damage'})
            for i in crit_damage:
                if i.text:
                    self.kritik_sansi.append((i.text))
            self.kritik_sansi.remove(' Crit. damage')
            self.kritik_sansi = "  ".join(self.kritik_sansi)



            move_speed = soup.find('div',{'data-source':'ms'})
            move_speed_value = move_speed.find_all('span')
            for i in move_speed_value:
                if i.text:
                    self.hareket_hizi.append((i.text))
            self.hareket_hizi = "  ".join(self.hareket_hizi)



            attack_range = soup.find('div',{'data-source':'range'})
            attack_range_value = attack_range.find_all('span')
            for i in attack_range_value:
                if i.text:
                    self.saldiri_menzili.append((i.text))
            self.saldiri_menzili = "  ".join(self.saldiri_menzili)
            
            

            base_attack_speed = soup.find('div',{'data-source':'attack speed'})
            for i in base_attack_speed:
                if i.text:
                    self.temel_saldiri_hizi.append((i.text))
            self.temel_saldiri_hizi.remove('Base AS')
            self.temel_saldiri_hizi = "  ".join(self.temel_saldiri_hizi)


            attack_windup = soup.find('div',{'data-source':'windup'})
            for i in attack_windup:
                if i.text:
                    self.saldiri_sonlandirma.append((i.text))
            self.saldiri_sonlandirma.remove('Attack windup')
            self.saldiri_sonlandirma = "  ".join(self.saldiri_sonlandirma)


            attack_speed_ratio = soup.find('div',{'data-source':'as ratio'})
            for i in attack_speed_ratio:
                if i.text:
                    self.saldiri_hizi_orani.append((i.text))
            self.saldiri_hizi_orani.remove('AS ratio')
            self.saldiri_hizi_orani = "  ".join(self.saldiri_hizi_orani)


            bonus_attack_speed = soup.find('div',{'data-source':'bonus as'})
            for i in bonus_attack_speed:
                if i.text:
                    self.bonus_saldiri_hizi.append((i.text))
            self.bonus_saldiri_hizi.remove('Bonus AS')
            self.bonus_saldiri_hizi = "".join(self.bonus_saldiri_hizi)


            gameplay_radius = soup.find('div',{'data-source':'gameplay radius'})
            for i in gameplay_radius:
                if i.text:
                    self.oyun_yaricap.append((i.text))
            self.oyun_yaricap.remove(' Gameplay radius')
            self.oyun_yaricap = "".join(self.oyun_yaricap)


            selection_radius = soup.find('div',{'data-source':'selection radius'})
            for i in selection_radius:
                if i.text:
                    self.secim_yaricap.append((i.text))
            self.secim_yaricap.remove(' Selection radius')
            self.secim_yaricap = "".join(self.secim_yaricap)


            pathing_radius = soup.find('div',{'data-source':'pathing radius radius'})
            for i in pathing_radius:
                if i.text:
                    self.yol_yaricap.append((i.text))
            self.yol_yaricap.remove(' Pathing radius')
            self.yol_yaricap = "".join(self.yol_yaricap)


            acquisition_radius = soup.find('div',{'data-source':'acquisition radius'})
            for i in acquisition_radius:
                if i.text:
                    self.edinme_yaricap.append((i.text))
            self.edinme_yaricap.remove(' Acq. radius')
            self.edinme_yaricap = "".join(self.edinme_yaricap)

            def diger_oyun_modlar(mod_ismi,ek_list):
                ozellik = soup.find('div',{'data-item-name':mod_ismi})
                ozellik_1 = ozellik.find('section',{'class':'pi-item pi-group pi-border-color'})
                ozellik_2 = ozellik_1.find_all('section',{'class':'pi-item pi-smart-group pi-border-color'})
                for i in ozellik_2:
                    a = i.find_all('div',{'class':'pi-smart-data-value pi-data-value pi-font pi-item-spacing pi-border-color'})
                    for b in a:
                        if b.text:
                            ek_list.append(b.text)
            
            diger_oyun_modlar('ARAM',self.aram)
            self.aram = "\n".join(self.aram)   
                
            diger_oyun_modlar('Nexus Blitz',self.nexus_blitz)
            self.nexus_blitz = "\n".join(self.nexus_blitz)
            
            diger_oyun_modlar('One For All',self.birimiz_hepimiz_icin)
            self.birimiz_hepimiz_icin = "\n".join(self.birimiz_hepimiz_icin)
            
            diger_oyun_modlar('Ultra Rapid Fire',self.urf)
            self.urf = "\n".join(self.urf)
            
            diger_oyun_modlar('Ultimate Spellbook',self.ulti_buyu_kitabi)
            self.ulti_buyu_kitabi = "\n".join(self.ulti_buyu_kitabi)
            
            diger_oyun_modlar('Arena',self.arena)
            self.arena = "\n".join(self.arena)

            cevirilicek_istatistik = [
                    ['CAN</p>','HEALTH</p>'],
                    ['MANA</p>','MANA</p>'],
                    ['SALDIRI GÜCÜ</p>','ATTACK DAMAGE</p>'],
                    ['HAREKET HIZI</p>','MOVEMENT SPEED</p>'],
                    ['ZIRH</p>','ARMOR</p>'],
                    ['BÜYÜ DİRENCİ</p>','MAGIC RESISTANCE</p>'],
                    ['CAN YENİLEME</p>','HEALTH REGENERATION</p>'],
                    ['MANA YENİLEME</p>','MANA REGENERATION</p>'],
                    ['KRİTİK VURUŞ ŞANSI</p>','CRITICAL STRIKE CHANCE</p>'],
                    ['SALDIRI MENZİLİ</p>','ATTACK RANGE</p>'],
                    ['TEMEL SALDIRI HIZI</p>','BASE ATTACK SPEED</p>'],
                    ['SALDIRI HIZI ORANI</p>','ATTACK SPEED RATIO</p>'],
                    ['SALDIRI SONLANDIRMA</p>','ATTACK WINDUP</p>'],
                    ['BONUS SALDIRI HIZI</p>','BONUS ATTACK SPEED</p>'],
                    ['OYUN YARIÇAPI</p>','GAMEPLAY RADIUS</p>'], 
                    ['SECİM YARIÇAPI</p>','SELECTION RADIUS</p>'], 
                    ['YOL YARIÇAPI</p>','PATHING RADIUS</p>'],
                    ['EDİNME YARIÇAPI</p>','ACQUISITION RADIUS</p>']        
                    ]
            cevirilicek_mod =[
                    ['Damage Dealt','Verilen Hasar '],
                    ['Damage Received','Alınan Hasar '],
                    ['Tenacity & Slow Resist','Dayanıklılık Ve Yavaşlatma Direnci '],
                    ['Ability Haste','Yetenek Hızı '],
                    ['Healing','İyileştirme '],
                    ['Shielding','Kalkan Gücü '],
                    ['Total Attack Speed','Toplam Saldırı Hızı '],
                    ['Move Speed','Hareket Hızı '],
                    ['Energy Regen','Enerji Yenileme '],
                ]
            if self.ui.radioButton_tr.isChecked() is True:
                for a in self.ui.frame_info.findChildren(QtWidgets.QLabel):
                    for c in cevirilicek_istatistik[-1::-1]:
                        b = a.text().replace(c[1],c[0])
                        a.setText(b)  
                for a in cevirilicek_mod:                 
                    self.aram = self.aram.replace(a[0],a[1])
                    self.nexus_blitz = self.nexus_blitz.replace(a[0],a[1])
                    self.birimiz_hepimiz_icin = self.birimiz_hepimiz_icin.replace(a[0],a[1])
                    self.urf = self.urf.replace(a[0],a[1])
                    self.ulti_buyu_kitabi = self.ulti_buyu_kitabi.replace(a[0],a[1])
                    self.arena = self.arena.replace(a[0],a[1])
                self.ui.label_birimizhepimizicin.setText('BİRİMİZ HEPİMİZ İÇİN')
                self.ui.label_ultibuyukitabi.setText('ULTİ BÜYÜ KİTABI')
                self.ui.buton_guncelle.setText('Manuel Güncelle')
                self.ui.checkBox_otomatikguncelle.setText('Otomatik Güncelle')
            if self.ui.radioButton_en.isChecked() is True:
                for a in self.ui.frame_info.findChildren(QtWidgets.QLabel):
                    for c in cevirilicek_istatistik:
                        b = a.text().replace(c[0],c[1])
                        a.setText(b)
                self.ui.label_birimizhepimizicin.setText('ONE FOR ALL')
                self.ui.label_ultibuyukitabi.setText('ULTI SPELLBOOK')
                self.ui.buton_guncelle.setText('Manual Update')
                self.ui.checkBox_otomatikguncelle.setText('Automatic Update')
                
            self.degerler()
        elif self.okunabilir_veri is False:
            pass
        
    def camp_arama_ac_kapat(self):        
        if self.arama_champ is True:
            self.ui.buton_samp_arama.setIcon(QtGui.QIcon('image\\icon\\arama_kapali.png'))
            self.ui.lineEdit_samp_arama.setText('')        
            self.ui.lineEdit_samp_arama.hide()
            self.ui.scrollArea_camp.setFixedHeight(self.ilk_scroll_olcu_dikey + 47)
            self.arama_champ = False
        elif self.arama_champ is False:
            self.ui.buton_samp_arama.setIcon(QtGui.QIcon('image\\icon\\arama_acik.png'))
            self.ui.scrollArea_camp.setFixedHeight(self.ilk_scroll_olcu_dikey)
            self.ui.lineEdit_samp_arama.show()
            self.ui.lineEdit_samp_arama.setFocus()
            self.arama_champ = True

    def bilgi_ac_kapat(self):
        if self.win2.isHidden() is True:       
            self.ui.buton_bilgi.setIcon(QtGui.QIcon('image\\icon\\bilgi_acik.png'))
            if self.ui.radioButton_tr.isChecked():
                self.win2.TR_REH()
            elif self.ui.radioButton_en.isChecked():
                self.win2.EN_REH()
            self.win2.show()        
        elif self.win2.isHidden() is False:         
            self.win2.close()   
    def rehber_kapat(self):         
        self.ui.buton_bilgi.setIcon(QtGui.QIcon('image\\icon\\bilgi_kapali.png'))
    def cevrimdisimod_ac_kapat(self):
        if self.cevrimdisimod is True:
            self.ui.buton_cevrimdisi.setIcon(QtGui.QIcon('image\\icon\\cevrimdisi_kapali.png'))
            self.cevrimdisimod = False
        elif self.cevrimdisimod is False:
            self.ui.buton_cevrimdisi.setIcon(QtGui.QIcon('image\\icon\\cevrimdisi_acik.png'))
            self.cevrimdisimod = True
    def camp_ses_ac_kapat(self):
        if self.campses_acik is True:
            self.ui.buton_sescamp.setIcon(QtGui.QIcon('image\\icon\\ses_kapali.png'))
            self.campses_acik = False
        elif self.campses_acik is False:
            self.ui.buton_sescamp.setIcon(QtGui.QIcon('image\\icon\\ses_acik.png'))
            self.campses_acik = True
    def modlari_ac_kapat(self):
        if self.mod_kapali is True:
            self.setFixedSize((self.ilk_boyut_olcu_yatay), self.height()) 
            self.ui.buton_modlar.setIcon(QtGui.QIcon('image\\icon\\mod_acik.png'))
            self.mod_kapali = False
        elif self.mod_kapali is False:
            self.setFixedSize(self.son_boyut_olcu_yatay ,self.height())
            self.ui.buton_modlar.setIcon(QtGui.QIcon('image\\icon\\mod_kapali.png'))
            self.mod_kapali = True
    def ayarlari_ac_kapat(self):
        if self.ayarlar_kapali is True:
            if self.ilerleme_durumu_kapali is True:
                self.setFixedSize(self.width() , self.ilk_boyut_olcu_dikey - 53) 
            if self.ilerleme_durumu_kapali is False:
                self.setFixedSize(self.width() , self.ilk_boyut_olcu_dikey) 
            self.ui.buton_ayarlar.setIcon(QtGui.QIcon('image\\icon\\ayarlar_acik.png'))
            self.ayarlar_kapali = False
        elif self.ayarlar_kapali is False:
            self.setFixedSize(self.width() , self.son_boyut_olcu_dikey)  
            self.ui.buton_ayarlar.setIcon(QtGui.QIcon('image\\icon\\ayarlar_kapali.png'))  
            self.ayarlar_kapali = True
    def ilerlemeyi_ac_kapat (self):
        if self.ilerleme_durumu_kapali is True:
            self.setFixedSize(self.width() , self.ilk_boyut_olcu_dikey)
            self.ui.buton_yuklemedurumu.setIcon(QtGui.QIcon('image\\icon\\ilerleme_acik.png'))
            self.ilerleme_durumu_kapali = False
        elif self.ilerleme_durumu_kapali is False:
            self.setFixedSize(self.width() , self.ilk_boyut_olcu_dikey - 53)
            self.ui.buton_yuklemedurumu.setIcon(QtGui.QIcon('image\\icon\\ilerleme_kapali.png'))
            self.ilerleme_durumu_kapali = True
    def manuel_guncelle(self):
        if self.update_thread.isRunning() is True:
            self.internet_yok.setIconPixmap(self.simge_bilgi)
            self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_kapat))
            self.internet_yok.setStandardButtons(QtWidgets.QMessageBox.Ok )
            butonok = self.internet_yok.button(QtWidgets.QMessageBox.Ok)
            butonok.setIcon(QtGui.QIcon(self.simge_tamam))
            if self.ui.radioButton_tr.isChecked():
                butonok.setText('TAMAM')       
                self.internet_yok.setWindowTitle('VERİLER GÜNCELLENİYOR !')
                self.internet_yok.setText('\n\nVeri seti zaten güncelleniyor.\nİlerleme durumunu ayarlardan\nkontrol edebilirsiniz.')
            elif self.ui.radioButton_en.isChecked():
                butonok.setText('OK')       
                self.internet_yok.setWindowTitle('DATA IS BEING UPDATED!')
                self.internet_yok.setText('\n\nThe dataset is already being updated.\nYou can check the progress in settings.')
            x = self.internet_yok.exec_()
            if x == QtWidgets.QMessageBox.Ok:
                pass  
        elif self.update_thread.isRunning() is False:
            self.update_thread.start()
    def veri_durum(self):
        self.ui.buton_yuklemedurumu.setIcon(QtGui.QIcon('image\\icon\\ilerleme_bildirim.png'))         
        self.ui.buton_ayarlar.setIcon(QtGui.QIcon('image\\icon\\ayarlar_bildirim.png'))  
        toplamveri = len(self.champions)
        veribasinailerleme = 100/toplamveri
        self.ilerlemedurumu_proggres += veribasinailerleme
        self.ui.progressBar_veriguncelle.setValue(round(self.ilerlemedurumu_proggres))
    def progresi_sifirla(self):
        self.internet_yok.setIconPixmap(self.simge_guncelle)
        self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_bilgi))
        self.internet_yok.setStandardButtons(QtWidgets.QMessageBox.Ok )
        butonok = self.internet_yok.button(QtWidgets.QMessageBox.Ok) 
        butonok.setIcon(QtGui.QIcon(self.simge_tamam))
        if self.ui.radioButton_tr.isChecked():
            self.internet_yok.setWindowTitle('VERİ DURUMU !')
            self.internet_yok.setText('\n\nVerilerin güncellenmesi\nbaşarıyla gerçekleşti!')
            butonok.setText('TAMAM')
        elif self.ui.radioButton_en.isChecked():
            self.internet_yok.setWindowTitle('DATA STATUS !')
            self.internet_yok.setText('\n\nUpdating the data\nwas successful!')
            butonok.setText('OK')
        x = self.internet_yok.exec_()
        if x == QtWidgets.QMessageBox.Open:
            pass
        self.ilerlemedurumu_proggres = 0
        if self.ayarlar_kapali is True:        
            self.ui.buton_ayarlar.setIcon(QtGui.QIcon('image\\icon\\ayarlar_kapali.png'))  
        elif self.ayarlar_kapali is False:
            self.ui.buton_ayarlar.setIcon(QtGui.QIcon('image\\icon\\ayarlar_acik.png'))  
        if self.ilerleme_durumu_kapali is True:        
            self.ui.buton_yuklemedurumu.setIcon(QtGui.QIcon('image\\icon\\ilerleme_kapali.png'))         
        elif self.ilerleme_durumu_kapali is False:
            self.ui.buton_yuklemedurumu.setIcon(QtGui.QIcon('image\\icon\\ilerleme_acik.png'))

    def kullanici_secimlerini_yukle(self):
        try:        
            if exe_is_running is True:
                os.chdir('..')
                with open('LOL Bilgileri\\config.json','r', encoding='UTF-8') as files:         
                    secimler = json.load(files)
                    os.chdir(sys._MEIPASS) 
            elif exe_is_running is False:
                with open('bilgiler\\config.json','r', encoding='UTF-8') as files:
                    secimler = json.load(files)
            try:        
                if secimler['otomatik_guncelleme'] == True:
                    self.ui.checkBox_otomatikguncelle.setChecked(True)
                if secimler['ingilizce_secim'] == True:
                    self.ui.radioButton_en.setChecked(True)
                if secimler['cevrimdisi_modu'] == True:
                    self.cevrimdisimod = True
                    self.ui.buton_cevrimdisi.setIcon(QtGui.QIcon('image\\icon\\cevrimdisi_acik.png'))       
                if secimler['sampiyon_ses'] == False:
                    self.campses_acik = False
                    self.ui.buton_sescamp.setIcon(QtGui.QIcon('image\\icon\\ses_kapali.png'))
            except KeyError:        
                pass   
        except FileNotFoundError:        
            pass
    def degerler(self):
        self.ui.label_can_deger.setText(self.can_bilgi)
        self.ui.label_mana_deger.setText(self.mana_bilgi)
        self.ui.label_saldirigucu_deger.setText(self.saldiri_gücü)
        self.ui.label_harekethizi_deger.setText(self.hareket_hizi)
        self.ui.label_zirh_deger.setText(self.zirh)
        self.ui.label_buyudirenci_deger.setText(self.buyu_direnci)
        self.ui.label_canyenileme_deger.setText(self.can_yenilenmesi)
        self.ui.label_manayenileme_deger.setText(self.mana_yenilenmesi)
        self.ui.label_kritiksansi_deger.setText(self.kritik_sansi)
        self.ui.label_saldirimenzili_deger.setText(self.saldiri_menzili)
        self.ui.label_temelsaldirihizi_deger.setText(self.temel_saldiri_hizi)
        self.ui.label_saldirihiziorani_deger.setText(self.saldiri_hizi_orani)
        self.ui.label_saldirisonlandirma_deger.setText(self.saldiri_sonlandirma)
        self.ui.label_bonussaldirihizi_deger.setText(self.bonus_saldiri_hizi)
        self.ui.label_oyunyaricap_deger.setText(self.oyun_yaricap)
        self.ui.label_secimyaricap_deger.setText(self.secim_yaricap)
        self.ui.label_yolyaricap_deger.setText(self.yol_yaricap)
        self.ui.label_edinmeyaricap_deger.setText(self.edinme_yaricap)
        self.ui.label_aram_deger.setText(self.aram)
        self.ui.label_nexusblitz_deger.setText(self.nexus_blitz)
        self.ui.label_birimizhepimizicin_deger.setText(self.birimiz_hepimiz_icin)
        self.ui.label_urf_deger.setText(self.urf)
        self.ui.label_ultibuyukitabi_deger.setText(self.ulti_buyu_kitabi)
        self.ui.label_arena_deger.setText(self.arena)
    def deger_hizala(self):
        self.ui.label_can_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_mana_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_saldirigucu_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_harekethizi_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_zirh_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_buyudirenci_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_canyenileme_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_manayenileme_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_kritiksansi_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_saldirimenzili_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_temelsaldirihizi_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_saldirihiziorani_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_saldirisonlandirma_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_bonussaldirihizi_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_oyunyaricap_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_secimyaricap_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_yolyaricap_deger.setContentsMargins(20,0,0,0) 
        self.ui.label_edinmeyaricap_deger.setContentsMargins(20,0,0,0) 
    def camp_name_btn(self):
        self.baglanti_yok = True
        while self.baglanti_yok:
            try:
                url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions/Base_statistics'
                html = requests.get(url).content    
                if requests.get(url).status_code != 200:        
                    html = urllib.request.urlopen(url)
                    if urllib.request.urlopen(url).code != 200:         
                        http = urllib3.PoolManager()
                        html = http.request('GET',url).data
                        if http.request('GET',url).status != 200:           
                            if exe_is_running is True:
                                os.chdir('..')
                                with open('LOL Bilgileri\\camp_name.json','r', encoding='UTF-8') as files:
                                    self.champions = json.load(files)
                                os.chdir(sys._MEIPASS) 
                            elif exe_is_running is False:
                                with open('bilgiler\\camp_name.json','r', encoding='UTF-8') as files:
                                    self.champions = json.load(files)
                            self.baglanti_yok = False
                soup = BeautifulSoup(html,'html.parser')    
                self.champions = []
                liste = soup.select('span:nth-child(2)')
                for i in liste:
                    isim = i.select('a')
                    for i in isim:
                        champ_name = i.get('title')
                        if champ_name.endswith('/LoL'):    
                            champ_name = champ_name.rstrip('oL')     
                            champ_name = champ_name.rstrip('/')
                            self.champions.append(champ_name)
                self.champions.remove('Kled & Skaarl')
                self.champions.remove('Nunu & Willump')
                self.champions.remove('Mega Gnar')
                self.champions.append('Nunu')
                self.champions.sort()
                if exe_is_running is True:
                    os.chdir('..')
                    try:
                        os.chdir('LOL Bilgileri')          
                    except:
                        pass
                    with open('camp_name.json','w', encoding='UTF-8') as files:
                        json.dump(self.champions,files,ensure_ascii=False,indent=1)
                    os.chdir(sys._MEIPASS) 
                elif exe_is_running is False:
                    with open('bilgiler\\camp_name.json','w', encoding='UTF-8') as files:
                        json.dump(self.champions,files,ensure_ascii=False,indent=1)
                self.baglanti_yok = False
                if self.ui.checkBox_otomatikguncelle.isChecked():      
                    self.update_thread.start()
                self.islem_devam = True
                
            except requests.exceptions.ConnectionError  :
                self.islem_devam = False
                self.internet_yok.setIconPixmap(self.simge_bilgi)
                self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_internet))
                self.internet_yok.setStandardButtons(QtWidgets.QMessageBox.Retry  | QtWidgets.QMessageBox.Close |  QtWidgets.QMessageBox.Open )
                butonretry = self.internet_yok.button(QtWidgets.QMessageBox.Retry)        
                butonretry.setIcon(QtGui.QIcon(self.simge_yenile))
                butonclose = self.internet_yok.button(QtWidgets.QMessageBox.Close) 
                butonclose.setIcon(QtGui.QIcon(self.simge_kapat))
                butonopen = self.internet_yok.button(QtWidgets.QMessageBox.Open) 
                butonopen.setIcon(QtGui.QIcon(self.simge_cevrimdisi))
                if self.ui.radioButton_tr.isChecked():
                    self.internet_yok.setWindowTitle('BAĞLANTI YOK !')
                    self.internet_yok.setText('\nUygulamamız verileri internetten\ngüncel olarak çekmektedir.\nLütfen internet bağlantısı\nsağladıktan sonra tekrar deneyin!\nYada çevrimdışı modu kullanın.\nTekrar Denemek İstermisiniz ?')
                    butonretry.setText('TEKRAR DENE')  
                    butonopen.setText('ÇEVRİMDIŞI MOD') 
                    butonclose.setText('KAPAT')
                elif self.ui.radioButton_en.isChecked():
                    self.internet_yok.setWindowTitle('NO CONNECTION !')
                    self.internet_yok.setText('\nOur application pulls up-to-date\ndata from the internet.Please\ntry again after establishing an internet\nconnection! Or use offline mode.\nWould you like to try again ?')
                    butonretry.setText('TRY AGAİN')  
                    butonopen.setText('OFFLİNE MOD') 
                    butonclose.setText('CLOSE')
                x = self.internet_yok.exec_()
                if x == QtWidgets.QMessageBox.Retry:
                    pass    
                elif x == QtWidgets.QMessageBox.Open:
                    if exe_is_running is True:
                        os.chdir('..')
                        os.chdir('LOL Bilgileri')
                        try:
                            with open('camp_name.json','r', encoding='UTF-8') as files:         
                                self.champions = json.load(files)
                            os.chdir(sys._MEIPASS) 
                        except FileNotFoundError:
                            os.chdir(sys._MEIPASS)
                            with open('bilgiler\\camp_name.json','r', encoding='UTF-8') as files:
                                self.champions = json.load(files)
                    elif exe_is_running is False:
                        with open('bilgiler\\camp_name.json','r', encoding='UTF-8') as files:
                            self.champions = json.load(files)
                    self.baglanti_yok = False
                    self.cevrimdisimod = True
                    self.ui.buton_cevrimdisi.setIcon(QtGui.QIcon('image\\icon\\cevrimdisi_acik.png'))
                elif x == QtWidgets.QMessageBox.Close:
                    self.baglanti_yok = False
                    sys.exit()      
    def veri_guncelleme_basarisiz(self):
        self.internet_yok.setIconPixmap(self.simge_bilgi)
        self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_internet))
        self.internet_yok.setStandardButtons(QtWidgets.QMessageBox.Cancel  |  QtWidgets.QMessageBox.Retry  | QtWidgets.QMessageBox.Close  )
        butonretry = self.internet_yok.button(QtWidgets.QMessageBox.Retry)       
        butonretry.setIcon(QtGui.QIcon(self.simge_yenile))
        butoncancel = self.internet_yok.button(QtWidgets.QMessageBox.Cancel) 
        butoncancel.setIcon(QtGui.QIcon(self.simge_tamam))
        butonclose = self.internet_yok.button(QtWidgets.QMessageBox.Close) 
        butonclose.setIcon(QtGui.QIcon(self.simge_kapat))
        if self.ui.radioButton_tr.isChecked():
            self.internet_yok.setWindowTitle('BAĞLANTI YOK !')
            self.internet_yok.setText('\n\nİnternet bağlantısı sağlanamadığı\nveya kesildiği için veriler güncellenemedi!\nLütfen daha sonra tekrar deneyin.')
            butonretry.setText('TEKRAR DENE') 
            butoncancel.setText('TAMAM')
            butonclose.setText('UYGULAMADAN ÇIK')
        elif self.ui.radioButton_en.isChecked():
            self.internet_yok.setWindowTitle('NO CONNECTION !')
            self.internet_yok.setText('\n\nThe data could not be updated\nbecause the internet connection was\nnot available or was interrupted!\nPlease try again later.')
            butonretry.setText('TRY AGAİN') 
            butoncancel.setText('OK')
            butonclose.setText('EXIT APPLICATION')
        x = self.internet_yok.exec_()
        if x == QtWidgets.QMessageBox.Retry:
            pass    
        elif x == QtWidgets.QMessageBox.Cancel:
            pass    
        elif x == QtWidgets.QMessageBox.Close:
            self.close()
    def closeEvent(self, event):        
        tercihler = {
            'otomatik_guncelleme':self.ui.checkBox_otomatikguncelle.isChecked(),
            'ingilizce_secim':self.ui.radioButton_en.isChecked(),
            'cevrimdisi_modu':self.cevrimdisimod,
            'sampiyon_ses':self.campses_acik
        } 
        
        if exe_is_running is True:
            os.chdir('..')
            with open('LOL Bilgileri\\config.json','w', encoding='UTF-8') as files:
                json.dump(tercihler,files,ensure_ascii=False,indent=1)    
            os.chdir(sys._MEIPASS) 
        elif exe_is_running is False:
            with open('bilgiler\\config.json','w', encoding='UTF-8') as files:
                json.dump(tercihler,files,ensure_ascii=False,indent=1)                  

        if self.update_thread.isRunning() is True:
            self.internet_yok.setIconPixmap(self.simge_bilgi)
            self.internet_yok.setWindowIcon(QtGui.QIcon(self.simge_kapat))
            self.internet_yok.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            butonok = self.internet_yok.button(QtWidgets.QMessageBox.Ok)
            butonok.setIcon(QtGui.QIcon(self.simge_guncelle))
            butoncancel = self.internet_yok.button(QtWidgets.QMessageBox.Cancel)
            butoncancel.setIcon(QtGui.QIcon(self.simge_kapat))
            if self.ui.radioButton_tr.isChecked():
                self.internet_yok.setWindowTitle('VERİLER GÜNCELLENİYOR !')
                self.internet_yok.setText('\n\nVeri seti güncelleniyor.\nYinede çıkış yapılsın mı?\n(Veri seti güncellemesinin yarıda\nbırakılması önerilmez)')
                butonok.setText('GÜNCELLE VE ÇIK')  
                butoncancel.setText('ÇIK') 
            elif self.ui.radioButton_en.isChecked():
                self.internet_yok.setWindowTitle('DATA IS BEING UPDATED !')
                self.internet_yok.setText('\n\nThe data set is being updated.\nShould I log out anyway?\n(Aborting the dataset\nupdate is not recommended)')
                butonok.setText('UPDATE AND EXIT')  
                butoncancel.setText('EXIT') 
            x = self.internet_yok.exec_()
            if x == QtWidgets.QMessageBox.Ok:
                event.ignore()      
                self.update_thread.islemler_bitti.connect(self.son_thread_kontrolu)        
            elif x == QtWidgets.QMessageBox.Cancel:
                self.update_thread.guncelleme()     
                self.update_thread.wait()
        elif self.update_thread.isRunning() is False:
            event.accept()
    def son_thread_kontrolu(self):
        if self.update_thread.isRunning() is False :
            self.close()
        if self.update_thread.isRunning() is True :
            self.update_thread.wait()
            self.close()


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Stats()
    win.show()
    sys.exit(app.exec_())

app()