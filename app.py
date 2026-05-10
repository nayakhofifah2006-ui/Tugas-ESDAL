import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Simulasi Harga Emas - Kelompok 10", layout="wide")

st.title("📊 Alat Simulasi Harga & Mekanisme Pasar Emas")
st.markdown("Berdasarkan Studi Kasus: **PT. Merdeka Copper Gold Tbk**")

# Sidebar - Parameter dari Dokumen
st.sidebar.header("Parameter Model (Data Modul)")
a = st.sidebar.number_input("Konstanta Harga (a)", value=2791.458) # [cite: 15, 38]
b = st.sidebar.number_input("Koefisien Permintaan (b)", value=0.0071036, format="%.7f") # 
mc = st.sidebar.number_input("Biaya Marginal (MC)", value=4943.21) # 

# 1. Mekanisme Pasar
st.header("📈 Simulasi Mekanisme Pasar")
market_type = st.selectbox("Pilih Struktur Pasar:", ["Persaingan Sempurna", "Monopoli", "Oligopoli (Cournot)"])

def calculate_market(market_type, a, b, mc):
    if market_type == "Persaingan Sempurna":
        # P = MC
        q_opt = (a - mc) / b if a > mc else 0
        p_opt = mc if a > mc else a
    elif market_type == "Monopoli":
        # MR = MC -> a - 2bQ = MC
        q_opt = (a - mc) / (2 * b) if a > mc else 0
        p_opt = a - (b * q_opt)
    else: # Oligopoli (2 Pemain)
        # Qi = (a - mc) / 3b
        q_total = (2 * (a - mc)) / (3 * b) if a > mc else 0
        q_opt = q_total
        p_opt = a - (b * q_total)
    
    return q_opt, p_opt

q_res, p_res = calculate_market(market_type, a, b, mc)

col1, col2 = st.columns(2)
col1.metric("Volume Produksi Optimal (Q)", f"{q_res:,.2f} oz")
col2.metric("Harga Optimal (P)", f"US$ {p_res:,.2f}")

# 2. Visualisasi Kurva
st.subheader("Kurva Permintaan vs Biaya Marginal")
q_range = np.linspace(0, (a/b)*1.2, 100)
p_demand = a - (b * q_range)

fig, ax = plt.subplots()
ax.plot(q_range, p_demand, label="Permintaan (P)", color='blue')
ax.axhline(y=mc, color='red', linestyle='--', label="Marginal Cost (MC)")
ax.scatter(q_res, p_res, color='black', zorder=5, label="Titik Keseimbangan")

ax.set_xlabel("Kuantitas (Q)")
ax.set_ylabel("Harga (P)")
ax.legend()
st.pyplot(fig)

# 3. Refleksi Ekonomi (Data Modul)
st.info(f"""
**Catatan Analisis:**
* Berdasarkan data historis 2017-2024, MC rata-rata adalah **{mc}**. [cite: 23]
* Hasil regresi menunjukkan $R^2$ sebesar **37.93%**, yang berarti faktor eksternal sangat dominan dalam menentukan harga sesungguhnya. [cite: 19, 20]
""")
