import streamlit as st

def main():
    st.title("Prueba de Interfaz en Streamlit")
    st.write("Este es un script de prueba para verificar la carga de la interfaz.")

    # Campo de texto
    keywords_input = st.text_area("Ingresa palabras clave (separadas por comas):")

    # Botón de análisis (sin funcionalidad)
    if st.button("Analizar PDFs"):
        st.write("Botón de análisis presionado.")
        if keywords_input:
            st.write("Palabras clave ingresadas:", keywords_input)
        else:
            st.warning("Por favor, ingresa al menos una palabra clave.")

    # Botón de descarga (sin funcionalidad)
    if st.button("Descargar Resultados"):
        st.write("Descarga solicitada. (Sin archivo)")

    # Mensaje final
    st.write("Interfaz cargada correctamente.")

if __name__ == "__main__":
    main()
