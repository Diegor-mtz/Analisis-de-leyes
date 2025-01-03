import fitz  # PyMuPDF
import spacy
import streamlit as st
import pandas as pd
from collections import Counter, defaultdict

# Cargar el modelo de spaCy
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    from spacy.cli import download
    download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

# Función para extraer texto del PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    pages = []
    for page in doc:
        page_text = page.get_text("text")
        text += page_text
        pages.append(page_text)
    return text, pages

# Función para procesar el texto y extraer los verbos
def extract_verbs(text, pages):
    doc = nlp(text)
    verb_counts = Counter()
    verb_forms = defaultdict(set)
    verb_pages = defaultdict(set)
    verb_pos = defaultdict(set)  # Almacenar categorías gramaticales

    for page_num, page_text in enumerate(pages, start=1):
        page_doc = nlp(page_text)
        for token in page_doc:
            if token.pos_ == "VERB":
                verb_counts[token.lemma_] += 1
                verb_forms[token.lemma_].add(token.text)
                verb_pages[token.lemma_].add(page_num)
                verb_pos[token.lemma_].add(token.tag_)  # Almacenar POS (tiempo/verbo)

    data = [
        {
            "Verbo Lematizado": verb,
            "Frecuencia": count,
            "Formas Originales": ", ".join(verb_forms[verb]),
            "POS": ", ".join(verb_pos[verb]),  # Añadir POS
            "Páginas": ", ".join(map(str, sorted(verb_pages[verb])))
        }
        for verb, count in verb_counts.most_common(5)
    ]
    
    return pd.DataFrame(data)

# Función para verificar verbos ingresados manualmente
def check_manual_verbs(pages, manual_verbs):
    verb_counts = Counter()
    verb_forms = defaultdict(set)
    verb_pages = defaultdict(set)
    verb_pos = defaultdict(set)

    for page_num, page_text in enumerate(pages, start=1):
        page_doc = nlp(page_text)
        for token in page_doc:
            if token.lemma_ in manual_verbs:
                verb_counts[token.lemma_] += 1
                verb_forms[token.lemma_].add(token.text)
                verb_pages[token.lemma_].add(page_num)
                verb_pos[token.lemma_].add(token.tag_)

    data = [
        {
            "Verbo Lematizado": verb,
            "Frecuencia": count,
            "Formas Originales": ", ".join(verb_forms[verb]),
            "POS": ", ".join(verb_pos[verb]),
            "Páginas": ", ".join(map(str, sorted(verb_pages[verb])))
        }
        for verb, count in verb_counts.items()
    ]
    
    return pd.DataFrame(data)

# Interfaz de Streamlit
def main():
    st.title("Análisis de Verbos en PDF con spaCy")
    st.write("Sube un archivo PDF y obtén los 5 verbos más frecuentes con sus formas originales, POS y páginas.")

    uploaded_file = st.file_uploader("Sube tu PDF aquí", type=["pdf"])

    manual_input = st.text_area("Ingresa verbos manualmente (separados por comas)")

    if uploaded_file:
        with st.spinner("Procesando PDF..."):
            text, pages = extract_text_from_pdf(uploaded_file)
            results_df = extract_verbs(text, pages)
            st.success("¡Análisis completado!")
            
            # Mostrar resultados en tabla
            st.write("### Top 5 Verbos Más Comunes")
            st.dataframe(results_df)

            # Verificación de verbos manuales
            if manual_input:
                manual_verbs = [v.strip().lower() for v in manual_input.split(",")]
                manual_df = check_manual_verbs(pages, manual_verbs)

                st.write("### Resultados de Verbos Ingresados Manualmente")
                if not manual_df.empty:
                    st.dataframe(manual_df)
                else:
                    st.write("No se encontraron coincidencias con los verbos ingresados.")

            # Botón para descargar CSV
            csv = results_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("Descargar resultados como CSV", csv, "resultados_verbos.csv", "text/csv")

if __name__ == "__main__":
    main()
