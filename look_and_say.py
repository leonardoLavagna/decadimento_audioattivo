import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import groupby
from collections import Counter
import math


# --------------------------------------------------------------
# Funzioni ausiliarie
# --------------------------------------------------------------
def look_and_say(s):
    result = ''
    for digit, group in groupby(s):
        count = len(list(group))
        result += str(count) + digit
    return result


def generate_sequence(start, steps):
    sequence = [start]
    for _ in range(steps):
        sequence.append(look_and_say(sequence[-1]))
    return sequence


def compute_statistics(sequence):
    stats = []
    for s in sequence:
        counter = Counter(s)
        total = len(s)
        entropy = -sum((count / total) * math.log2(count / total) for count in counter.values())
        stats.append({
            "length": total,
            "1s": counter.get('1', 0),
            "2s": counter.get('2', 0),
            "3s": counter.get('3', 0),
            "entropy": entropy
        })
    return pd.DataFrame(stats)


def estimate_growth(sequence):
    lengths = [len(s) for s in sequence]
    ratios = [lengths[i+1]/lengths[i] for i in range(len(lengths)-1) if lengths[i] > 0]
    return ratios


# --------------------------------------------------------------
# Interfaccia Streamlit
# --------------------------------------------------------------
st.set_page_config(page_title="Decadimento Audioattivo", layout="centered")
st.title("🎲 Decadimento Audioattivo (Look-and-Say)")

# Input
start_string = st.text_input("🔡 Inserisci la stringa iniziale:", "1")
steps = st.slider("🔁 Numero di iterazioni:", min_value=1, max_value=50, value=10)
# Validazione input
if not start_string.isdigit() or "0" in start_string:
    st.error("La stringa iniziale deve contenere solo cifre da 1 a 3 (niente zeri o altri numeri).")
    st.stop()
  
# Generazione sequenza
sequence = generate_sequence(start_string, steps)
stats_df = compute_statistics(sequence)
# Output testuale
with st.expander("📜 Visualizza la sequenza completa"):
    for i, s in enumerate(sequence):
        st.text(f"{i}: {s}")

# Grafico lunghezze
st.subheader("📏 Crescita della lunghezza")
lengths = stats_df["length"]
fig1, ax1 = plt.subplots()
ax1.plot(range(len(lengths)), lengths, marker="o")
ax1.set_xlabel("Iterazione")
ax1.set_ylabel("Lunghezza")
st.pyplot(fig1)

# Grafico frequenze
st.subheader("📊 Frequenza delle cifre")
fig2, ax2 = plt.subplots()
ax2.plot(stats_df.index, stats_df["1s"], label="1", marker="o")
ax2.plot(stats_df.index, stats_df["2s"], label="2", marker="o")
ax2.plot(stats_df.index, stats_df["3s"], label="3", marker="o")
ax2.set_xlabel("Iterazione")
ax2.set_ylabel("Frequenza assoluta")
ax2.legend()
st.pyplot(fig2)

# Entropia
st.subheader("🧠 Entropia Shannon delle stringhe")
fig3, ax3 = plt.subplots()
ax3.plot(stats_df.index, stats_df["entropy"], marker="o")
ax3.set_xlabel("Iterazione")
ax3.set_ylabel("Entropia (bit)")
st.pyplot(fig3)

# Costante cosmologica stimata
st.subheader("📈 Stima empirica della costante cosmologica di Conway (λ)")
ratios = estimate_growth(sequence)
st.line_chart(ratios)
avg_lambda = np.mean(ratios[-5:]) if len(ratios) >= 5 else np.mean(ratios)
st.success(f"λ stimata negli ultimi passi: **{avg_lambda:.6f}**")

# Esporta tabella
st.download_button("📥 Scarica statistiche CSV", data=stats_df.to_csv(index=False), file_name="statistiche_audioattive.csv")

# Footer
st.caption("Creato con ❤️ e Streamlit — Basato sul teorema cosmologico di Conway.")
