import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import groupby
from collections import Counter
import math

# -------------------------------
# Atomi audioattivi (versione compatta)
# -------------------------------
KNOWN_ATOMS = [
    "1112", "1113", "1122", "1123", "1132", "1133",
    "1211", "1212", "1221", "1231", "1311", "1321",
    "1322", "1331", "2112", "2122", "2132", "2211",
    "2311", "3122", "3211", "3311"
]

# -------------------------------
# Funzioni ausiliarie
# -------------------------------

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

def find_known_atoms(term, atom_list):
    found = []
    for atom in atom_list:
        if atom in term:
            found.append(atom)
    return found

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Decadimento Audioattivo", layout="centered")
st.title("🎲 Decadimento Audioattivo (Look-and-Say)")

menu = st.sidebar.radio("📚 Menu", ["Simulazione", "Analisi atomi", "Dati & grafici"])

# Input globale
start_string = st.text_input("🔡 Inserisci la stringa iniziale:", "1")
steps = st.slider("🔁 Numero di iterazioni:", min_value=1, max_value=50, value=10)

if not start_string.isdigit() or "0" in start_string:
    st.error("La stringa iniziale deve contenere solo cifre da 1 a 3 (niente zeri o altri numeri).")
    st.stop()

sequence = generate_sequence(start_string, steps)
stats_df = compute_statistics(sequence)

# -------------------------------
# SIMULAZIONE
# -------------------------------
if menu == "Simulazione":
    st.subheader("📜 Sequenza generata")
    with st.expander("Visualizza la sequenza completa"):
        for i, s in enumerate(sequence):
            st.text(f"{i}: {s}")

# -------------------------------
# ANALISI ATOMI
# -------------------------------
elif menu == "Analisi atomi":
    st.subheader("🧬 Rilevamento di atomi audioattivi ufficiali")
    atom_data = []
    for i, term in enumerate(sequence):
        found = find_known_atoms(term, KNOWN_ATOMS)
        atom_data.append({
            "Iterazione": i,
            "Atomi rilevati": ", ".join(found) if found else "—",
            "Numero atomi": len(found)
        })

    atom_df = pd.DataFrame(atom_data)
    st.dataframe(atom_df)

    if atom_df["Numero atomi"].sum() == 0:
        st.warning("Nessun atomo ufficiale rilevato nelle stringhe generate.")
    else:
        st.success(f"Totale atomi rilevati: {atom_df['Numero atomi'].sum()}")

# -------------------------------
# DATI & GRAFICI
# -------------------------------
elif menu == "Dati & grafici":
    st.subheader("📏 Crescita della lunghezza")
    fig1, ax1 = plt.subplots()
    ax1.plot(stats_df.index, stats_df["length"], marker="o")
    ax1.set_xlabel("Iterazione")
    ax1.set_ylabel("Lunghezza")
    st.pyplot(fig1)

    st.subheader("📊 Frequenza delle cifre")
    fig2, ax2 = plt.subplots()
    ax2.plot(stats_df.index, stats_df["1s"], label="1", marker="o")
    ax2.plot(stats_df.index, stats_df["2s"], label="2", marker="o")
    ax2.plot(stats_df.index, stats_df["3s"], label="3", marker="o")
    ax2.set_xlabel("Iterazione")
    ax2.set_ylabel("Frequenza")
    ax2.legend()
    st.pyplot(fig2)

    st.subheader("🧠 Entropia Shannon")
    fig3, ax3 = plt.subplots()
    ax3.plot(stats_df.index, stats_df["entropy"], marker="o")
    ax3.set_xlabel("Iterazione")
    ax3.set_ylabel("Entropia (bit)")
    st.pyplot(fig3)

    st.subheader("📈 Stima empirica di λ (costante di Conway)")
    ratios = estimate_growth(sequence)
    st.line_chart(ratios)
    if len(ratios) >= 5:
        avg_lambda = np.mean(ratios[-5:])
    else:
        avg_lambda = np.mean(ratios)
    st.success(f"λ stimata negli ultimi passi: **{avg_lambda:.6f}**")

    st.download_button("📥 Scarica CSV delle statistiche",
                       data=stats_df.to_csv(index=False),
                       file_name="statistiche_audioattive.csv")

# Footer
st.caption("Creato con ❤️ e Streamlit — Basato sul teorema cosmologico di Conway.")
