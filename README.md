# data-terbuka-id

Kumpulan Scrapy spider untuk mengumpulkan data dari situs-situs pemerintah.

# Instalasi

* Kloning repositori: `git clone git@github.com:seagatesoft/data-terbuka-id.git`

* Pastikan pada sistem Anda terinstal Python (virtualenv dan virtualenvwrapper juga disarankan)

* Install dependencies `pip install -r requirements.txt`

* Jalankan spider

## Spider yang tersedia

### Daftar Masjid

* Sumber data: http://simas.kemenag.go.id/index.php/profil/masjid/

* Menjalankan spider: `scrapy crawl simas.kemenag.go.id -o masjid.json` (akan mengumpulkan semua data masjid ke dalam file masjid.json)
