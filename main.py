#Yusuf Göktuğ Aydemir Python Masaüstü Uygulaması
#-----------------------------------------------
from ast import Index
import enum
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from panel import *


#Arayüz İşlemleri
#------------------------------------------------
uygulama = QApplication(sys.argv)
pencere =   QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

#Veritabanı İşlemleri
#-------------------------------------------------
import sqlite3

baglantı = sqlite3.connect("kayit.db")
islem = baglantı.cursor()
baglantı.commit()

table = islem.execute("Create Table if Not Exists Kayit(Ad text,Soyad text,Sirket text)")
baglantı.commit()

ui.tbl1.setHorizontalHeaderLabels(("Ad","Soyad","Şirket"))

def kayit_ekle():
    Ad = ui.lne1.text()
    Soyad = ui.lne2.text()
    Sirket = ui.cmb1.currentText()


    try:
        ekle ="insert into Kayit(Ad,Soyad,Sirket) values (?,?,?)"
        islem.execute(ekle,(Ad,Soyad,Sirket))
        baglantı.commit()
        ui.statusbar.showMessage("Kayıt Eklendi !",10000)
        kayit_listele()
    except:
        ui.statusbar.showMessage("Kayıt Eklenemedi. ",10000)

def kayit_listele():
    ui.tbl1.clear()
    ui.tbl1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ui.tbl1.setHorizontalHeaderLabels(("Ad","Soyad","Şirket"))
    sorgu = "select * from Kayit"
    islem.execute(sorgu)

    for indexSatir,kayitNumarasi in enumerate(islem):
        for IndexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tbl1.setItem(indexSatir,IndexSutun,QTableWidgetItem(str(kayitSutun)))

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere,"Silme Onayı","Silmek İstediğinize Emin Misiniz ? ")
    QMessageBox.Yes |QMessageBox.No

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tbl1.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "delete from Kayit where Ad = ?"

        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglantı.commit()
            ui.statusbar.showMessage("Kayıt Silindi.",10000)
            kayit_listele()
        except:
            ui.statusbar.showMessage("Kayıt Silinemedi.",10000)

    else:
        ui.statusbar.showMessage("İşlem İptal Edildi.",10000)


def sirkete_göre_listele():
    listelenecek_sirket = ui.cmb2.currentText()
    sorgu = "select * from Kayit where sirket = ?"
    islem.execute(sorgu,(listelenecek_sirket,))
    ui.tbl1.clear()
    ui.tbl1.setHorizontalHeaderLabels(("Ad","Soyad","Şirket"))
    for indexSatir,kayitNumarasi in enumerate(islem):
        for IndexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tbl1.setItem(indexSatir,IndexSutun,QTableWidgetItem(str(kayitSutun)))


            

#Butonlar
#---------------------

ui.btn1.clicked.connect(kayit_ekle)
ui.btn2.clicked.connect(kayit_sil)
ui.btn3.clicked.connect(sirkete_göre_listele)

kayit_listele()

sys.exit(uygulama.exec_())