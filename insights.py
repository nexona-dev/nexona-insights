import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import chardet

# Dosyanın kodlamasını otomatik tespit et
with open("sales_data.csv", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    detected_encoding = result["encoding"]
    print(f"Tespit edilen kodlama: {detected_encoding}")

# Tespit edilen kodlama ile oku
df = pd.read_csv("sales_data.csv", encoding=detected_encoding)

print("=== HAM VERİ ===")
print(df.head())
print(f"\nToplam satır: {len(df)}")

# 1. Müşteri isimlerini düzelt
df["Customer Name"] = df["Customer Name"].str.title()

# 2. Eksik değerleri medyan ile doldur
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
df["Price"] = df["Price"].fillna(df["Price"].median())

# 3. Tekrarları kaldır
df = df.drop_duplicates()

# 4. Yeni sütunlar ekle
df["Total"] = df["Quantity"] * df["Price"]
df["Order Date"] = pd.to_datetime(df["Order Date"])

print("\n=== TEMİZLENMİŞ VERİ ===")
print(df.head())
print(f"\nToplam satır: {len(df)}")

# 5. Analiz: Bölgeye göre toplam satış
region_sales = df.groupby("Region")["Total"].sum().sort_values(ascending=False)
print("\n=== BÖLGEYE GÖRE SATIŞ ===")
print(region_sales)

# 6. Görselleştirme
plt.figure(figsize=(10, 6))
sns.barplot(x=region_sales.index, y=region_sales.values, palette="viridis")
plt.title("Sales by Region (TL)")
plt.xlabel("Region")
plt.ylabel("Total Sales (TL)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("sales_by_region.png")
print("\nGrafik kaydedildi: sales_by_region.png")

# 7. Temizlenmiş veriyi kaydet
df.to_csv("cleaned_sales_data.csv", index=False, encoding="utf-8-sig")
print("Temizlenmiş veri kaydedildi: cleaned_sales_data.csv")
