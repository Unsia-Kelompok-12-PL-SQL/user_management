﻿
```markdown
# UTS PL SQL 12 - User Management

## Instalasi

Untuk menginstal paket yang diperlukan, jalankan perintah berikut:

```bash
pip install fastapi[all] uvicorn databases[postgresql] passlib[bcrypt] python-jose

## Konfigurasi Database

1.  Buat database dengan nama 'user_management'.
    
2.  Gantilah URL sesuai dengan kredensial PostgreSQL Anda pada file `database.py`. URL tersebut seharusnya memiliki format berikut:
`"postgresql://<postgres>:<admin>@localhost/user_management"` 
    

## Menjalankan Server

Untuk menjalankan server, gunakan perintah berikut:

bash

`uvicorn user_management.main:app --reload` 

Pastikan terminal berada di lokasinya parent dari directory "/user_management/". Jika tidak, arahkan terminal ke folder parent dengan perintah:

bash

```bash
cd ..
```
```
