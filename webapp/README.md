# jepara-furniture

Prerequisites:


- Python [Python 3.0 or later  installed](https://www.python.org/downloads/)
- mySQL - [Install Postgres.app for Mac](https://dev.mysql.com/downloads/installer/) (local development)

Guide berikut untuk command pada windows jika menggunakan linux atau mac mungkin akan sedikit berbeda

## Cara ingin membuat projek django (tidak wajib dilakukan untuk projek ini)

Bagian ini menjelaskan cara membuat app dengan django dari scracth atau kosong sehingga pembaca dapat membuat sendiri webapp django miliknya. Jika pembaca hanya ingin menjalankan dan mendevelop webapp ini bagian ini dapat di skip.

0. Aktifkan venv (OPTIONAL)

    Jika user tidak ingin membuat applikasi lanjutan dengan django lagi step ini bisa di skip. Step ini berguna untuk menginstall depedensi pada sebuah virtual env sehingga python tetap bersih, cth : jika memakai venv user install depedensi A, nah depedensi A atau modul A hanya akan ada atau terinstall ketika venv diaktifkan sehingga ketika membuat app lain depensi A tidak ada dan bisa diketahui depedensi apa saja yang dipakai, namun jika tidak menggunakan venv bisa maka depedensi akan ada pada python disave dan depedensi tidak perlu diaktifkan.

    cara aktifkan venv :

        install venv

     ```sh
    pip install virtualenv
    ```

        kemudian buat venv 

     ```sh
    virtualenv {{nama_env_yang_diinginkan}}
    ```

        aktifkan venv :
    
        ```sh
    path_to_venv_yang_dibuat/Scripts/activate
    ```

    kemudian masih di cmd yang sama pindah ke direktori pekerjaan.
    

1. Install django dengan cara buka command prompt dan jalankan perintah berikut :

    ```sh
    pip install django
    ```
    
2. Membuat project dengan perintah :

    ```sh
    django-admin startproject 'nama project yang diiginkan'
    ```

3. Dengan command prompt yang sama pindah ke direktori project :

    ```sh
    cd 'nama project'
    ```

4. Buat app pada project :

    command :
    ```sh
    django-admin startapp 'nama app yang diiginkan'
    ```

    Project bisa dibilang sebagai nama keseluruhan webapp sedangkan app adalah bagian dari project contoh app user, admin , staff dan bisa di breakdown menjadi beberapa app sesuai keiginan user.

5. Tambahkan app yang dibuat di project.

    pada direktori project yang dibuat ada folder dengan nama projcet tersebut pada folder itu buka dan ubah file setting.py dan tambahkan nama project anda pada installed apps

    contoh :
    sebelum :
    ```sh
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]
    ```

    sesudah :
    ```sh
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nama_app',
    ]
    ```
6. jika ingin menggunakan database yang bukan sqlite ubah setting.py tersebut juga pada bagian database.(OPTIONAL):

    Sebelum :
    ```sh
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
     }
    }
    ```

    sesudah :

    ```sh
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'law4',
        'USER': 'postgres',
        'PASSWORD': 'arif1234',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }
    ```

7. Migrasi data ke database.
    Jalankan command berikut setiap kali ingin mengubah table database.
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

8. Ubah urls.py dengan menambahkan untuk menambah path aplikasi.
    Urls.py berguna untuk menambah url aplikasi urls.py yang diubah adalah bagian di folder namaproject/urls.py.
    contoh : kode 
    path('user/',include('user.urls')),
    dengan menambah line diatas berarti seluruh url dari localhost:8000/user akan di jalankan handle oleh urls yang ada di user lalu pada user.urls kita menambah url routing yang kita inginkan.
    path('', views.land_page),
    1 line code diatas berarti url pada /user/ akan di handle oleh fungsi land_page yang ada di views.py
    path('login', views.login),
    1 line code diatas berarti url pada /user/login akan di handle oleh fungsi login yang ada di views.py
    jika ingin menambah url di /user maka tambahlah pada user/urls.py namun untuk url yang lain dapat ditambahkan di webapss langsung atau di urls lainnya setelah dari webapps.

9. Buat html untuk page.
    buatlah html untuk page sesuai urls routingnya contoh untuk seluruh urls /user/* buatlah file .html di user/templates/ jika folder templates belum ada buatlah folder tersebut lalu buat file html disana.

10. Buat fungsi untuk menreturn html agar sampai ke user.
    Ubah kode views.py dan masukkan nama fungsi sesuai pada urls yang ada sebelumnya dan masukkan di akhir fungsi tersebut
    return render(request , 'nama file html',html)

11. Jalankan webapps dengan cara menjalankan perintah berikut :

    ```sh
    python manage.py runserver
    ```

Sekian untuk bagian secara dasar pembuatan project django from scatch bukan untuk menjalankan project berikut.

## Cara menjalankan webapps di local komputer anda

0. Aktifkan venv (optional)
    Caranya sudah ada di tutorial diatas silahkan diikuti jika ingin , INI TIDAK WAJIB

1. Install semua depedensi ataupun modul yang dibutuhkan 
    Webapps ini menggunakan beberapa depedensi atau modul yang tidak terinstall default di python. Cara installasi dengan perintah :

    ```sh
    pip install -r requirements.txt
    ```

2. Konek ke mysql database.
    Karena mysql database setiap user berbeda maka ubahkan setting.py anda pada bagian database sesuai konfigurasi database anda. 

    contoh :

    sebelum :
    ```sh
        DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jepara_furniture',
        'USER': 'mysql',
        'PASSWORD': 'arif1234',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }
    ```

    sesusdah :

    ```sh
        DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nama database mysql schema yang diiginkan',
        'USER': 'nama user mysql anda',
        'PASSWORD': 'password mysql anda',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }
    ```
3. Migrasi database.
    Karena table databse pada schema anda pada awalnya seharusnya kosong maka database perlu di masukkan table sesuai yang dibutuhkan webapps dapat dijalankan dengan cara menjalankan perintah :
    
     ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Jalankan webapps.

    Jalankan webapss dengan perintah :
    ```sh
    python manage.py runserver
    ```
    maka webapps dapat anda lihat pada browser anda dengan url : 
    localhost:8000 atau bisa juga diakses dengan url
    127.0.0.1:8000

    jika port ingin diubah tidak 800 jalankan dengan perintah :

        ```sh
    python manage.py runserver port_number 
    ```

sekian cara menjalankan apps pada local sudah selesai yay.

## Sedikit tips untuk mengerti fungsi tiap file :

folder user berisi apps atau fitur untuk user.
folder staff berisi apps atau fitur untuk staff
folder admin berisi apps atau fitur untuk admin

pada file yang bernama views.py pada setiap folder berguna untuk mengatur logic dari aplikasi seperti mengambil data dari database , menrender html , menerima input form registrasi  dari user dan memprosesnya dst.

pada file urls.py berguna untuk routing url aplikasi seperti url localhost/user/login , localhost/user/register dan memilih fungsi views apa yang akan dipakai ketika url tersebut terpanggil.

file models.py berguna untuk django orm dimana jika kita menambah class pada models maka ketika menjalankan  perintah migrasi database maka database akan terubah, models dapat dikatakan sebagai penghubung untuk ke mysql sehingga seluruh table berbentuk class dan kolom di db berbentuk attribut dari class, jangan lupa jika setiap kali models.py diubah maka perintah migrasi harus dijalankan.

file .html sudah jelas berguna untuk html page yang dilihat oleh user. File .html  pasti berada di direktori templates sesuai dengan app fiturnya cth page untuk user maka file .html akan ada di /user/templates/  dst.

folder atau direktori static berguna untuk file-file static seperti image, css ,js yang dipakai oleh html untuk memperbagusnya.