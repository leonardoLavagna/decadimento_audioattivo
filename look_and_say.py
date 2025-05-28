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
    "3", "13", "1113", "3113", "111312", "132", "311332", "13221133112",
    "1113222", "1322113", "311311222113", "1113122113", "132113", "3113",
    "1113", "13", "3", "1113122113322113111221131221", "13211322211312113211",
    "311322113212221", "132211331222113112211", "311311222113111221131221",
    "111312211312113211", "132113212221", "3113112211", "11131221", "13211",
    "3112221", "1322113312211", "311311222113111221", "11131221131211",
    "13211321", "311311", "11131", "1321133112", "31131112", "111312",
    "132", "311332", "1113222", "13221133112", "3113112221131112",
    "111312211312", "1321132", "311311222", "11131221133112", "1321131112",
    "311312", "11132", "13112221133211322112211213322113",
    "312211322212221121123222113", "111312211312113221133211322112211213322113",
    "1321132122211322212221121123222113", "3113112211322112211213322113",
    "111312212221121123222113", "132112211213322113", "31121123222113",
    "111213322113", "123222113", "3113322113", "1113222113", "1322113",
    "311311222113", "1113122113", "132113", "3113", "1113", "13", "3",
    "13112221133211322112211213322112", "312211322212221121123222112",
    "111312211312113221133211322112211213322112", "1321132122211322212221121123222112",
    "3113112211322112211213322112", "111312212221121123222112", "132112211213322112",
    "31121123222112", "111213322112", "123222112", "3113322112", "1113222112",
    "1322112", "311311222112", "1113122112", "132112", "3112", "1112", "12"
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
st.markdown("""Questa applicazione ti permette di esplorare il [gioco look-and-say](https://it.wikipedia.org/wiki/Decadimento_audioattivo). Se ti interessa saperne di più vedi questo [blog post](https://geometrino.wordpress.com/2025/05/28/il-teorema-cosmologico-di-conway-raccontato-con-il-sorriso/)""")
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
