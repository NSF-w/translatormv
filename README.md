# TRANSLATOR RPG MAKER MV (VIA HP)
Translator RPG MAKER MV 

## Bahan

[Termux-FDROID](https://f-droid.org/repo/com.termux_1000.apk) / [Termux-PS](https://play.google.com/store/apps/details?id=com.termux)

[File Translator] #Nanti saja downloadnya via termux

## Tutorial

### 1. Install Termux

### 2. Buka termux dan ikuti perintah di bawah ini
### Setting termux, install python dan github

```
Note :
Tinggal copas saja dengan klik icon 2 kotak sebelah kanan disetiap command/perintahnya 
```

a. Setting perizinan storage untuk download python dan data file translator

```
termux-setup-storage
```

b. cek termux update dan upgrade

```
apt-get update
apt-get updgrade
```

c. Install Python

```
pkg install python
```

d. Install github

```
pkg install github
```

### 3. Membuat Folder Baru Di Internal HP dan download file translator nya

caranya ya tinggal ke file manajer bikin folder baru aja
contoh disini saya bikin folder namanya "rpgmv"

a. Masuk ke folder yang sudah dibikin tadi di internal hp via termux

```
cd /storage/emulated/0/rpgmv
```

b. Download file translator via termux

```
git clone https://github.com/NSF-w/translatormv/
```

### 4. Install requirement file agar bisa dijalankan 

a. masuk folder translatormv

```
cd /storage/emulated/0/rpgmv/translatormv
```

note : jika termux sudah dikeluarkan dengan perintah exit dan ingin masuk folder langsung maka tinggal tekan panah atas/bawah supaya memunculkan kodenya yang sudah tersimpan tanpa harus mengetik ulang

b. Install requirement 

```
pip install -r requirements.txt
```

### 5. Translate 

a. Copas semua file .json yang ada di data game rpg maker mv yang mau diterjemahkan ke folder translatormv/dialogs
- Copas menggunakan file manajer
- file .json lokasinya biasanya di nama game/www/data
- Copas file .json ke folder translatormv/dialogs

b. Menjalankan bot nya di termux

```
python bot.py -dl id
```

Note :
- edit replace.json untuk edit otomatis kata tertentu pada waktu menerjemahkan
- untuk mengganti terjemahan tinggal diubah "id" ke bahasa lainnya misalkan "en" untuk inggris, "jv" untuk jawa, "su" untuk sunda
contoh :
menerjemahkan bahasa apapun ke bahasa Inggris 

```
python bot.py -dl en
```

- Untuk cek list bahasa bisa di cek di [sini](https://cloud.google.com/translate/docs/languages?hl=id)

### Done otomatis translate 

### Untuk menjalankan nya lagi cukup ikuti langkah 4.a -> 5.a -> 5.b saja, tidak usah diulang dari awal
