# E-Commerce Public Dataset Dashboard

## Deskripsi Proyek

Proyek ini menganalisis E-Commerce Public Dataset untuk memahami performa revenue, kategori produk, segmentasi pelanggan berdasarkan RFM Analysis, serta kontribusi wilayah/state terhadap transaksi.

## Struktur Folder

submission/
├── dashboard/
│   ├── main_data.csv
│   ├── rfm_data.csv
│   ├── state_analysis.csv
│   ├── category_analysis.csv
│   └── dashboard.py
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
│   └── product_category_name_translation.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Cara Menjalankan Dashboard

1. Install library yang dibutuhkan:

pip install -r requirements.txt

2. Jalankan dashboard:

streamlit run dashboard/dashboard.py

## Link Dashboard

Link dashboard Streamlit Cloud ditulis pada file url.txt.