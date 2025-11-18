import streamlit as st
import spacy
import ca_core_news_sm # Necessitem aquesta importació si s'usa l'opció ca_core_news_sm.load()
from io import StringIO
import sys

# --- Configuració de la Pàgina Streamlit ---
st.set_page_config(page_title="Etiquetador Català (SpaCy) - Streamlit", layout="wide")

# Afegir el Logo de la UOC
st.image("202-nova-marca-uoc.jpg", width=200) 

st.title("Etiquetador Morfosintàctic Català amb SpaCy")

# --- Inicialització de l'Estat de la Sessió ---
if 'input_text_data' not in st.session_state:
    st.session_state['input_text_data'] = "" # Ús d'un nom de clau diferent per seguretat
if 'output_text_data' not in st.session_state:
    st.session_state['output_text_data'] = ""

# --- Funció de Callback per gestionar la pujada de fitxers ---
def handle_upload():
    """Llegeix el fitxer pujat i actualitza directament l'estat de la sessió."""
    uploaded_file = st.session_state.file_uploader_key
    if uploaded_file is not None:
        try:
            # Llegeix el contingut del fitxer de manera fiable
            text_a_etiquetar = uploaded_file.getvalue().decode("utf-8")
            # Actualitzem la clau de dades d'entrada
            st.session_state['input_text_data'] = text_a_etiquetar
            
        except Exception as e:
            st.error(f"Error llegint el fitxer: {e}")
            st.session_state['input_text_data'] = ""


# --- UI d'Entrada ---
st.subheader("Text d'Entrada")

col1, col2 = st.columns([1, 1])

with col1:
    st.file_uploader(
        "Puja un fitxer de text (.txt)",
        type=['txt'],
        key="file_uploader_key",
        on_change=handle_upload,
        label_visibility="collapsed"
    )

with col2:
    if st.button("Neteja Text d'Entrada"):
        st.session_state['input_text_data'] = ""
        st.session_state['output_text_data'] = ""
        st.rerun() 

# Àrea de text per a l'entrada (simplificat: l'entrada/sortida es fa directament amb la clau)
# El widget st.text_area ara llegeix i escriu directament a la clau 'input_text_data'
input_content = st.text_area(
    "Enganxa o edita el text:",
    value=st.session_state['input_text_data'],
    height=200,
    # El key="input_text_data" li diu a Streamlit que el valor d'aquest widget
    # HA DE SER el valor de st.session_state['input_text_data']
    key="input_text_data" 
)

# --- Funció d'Etiquetatge ---

@st.cache_resource 
def load_spacy_model():
    """Carrega el model SpaCy."""
    try:
        return ca_core_news_sm.load()
    except Exception as e:
        st.error(f"Error carregant el model SpaCy (ca_core_news_sm): {e}")
        st.stop()
        return None

def pos_tag_text(input_content):
    """Executa l'etiquetatge morfosintàctic sobre el text d'entrada."""
    if not input_content.strip():
        return "Error: No hi ha text per analitzar."

    try:
        POSmodel_spacy = load_spacy_model()
    except Exception as e:
        return f"Error: No s'ha pogut carregar el model SpaCy. {e}"

    mode = "coarse" 
    output_lines = []

    for linia in input_content.split('\n'):
        linia = linia.rstrip()
        if not linia.strip():
            output_lines.append("")
            continue

        taggedtokens = POSmodel_spacy(linia)
        ttsentence = []
        for token in taggedtokens:
            form = token.text
            lemma = token.lemma_
            if mode == "fine":
                tag = token.tag_
            elif mode == "coarse":
                tag = token.pos_
            
            ttsentence.append(f"{form}|{lemma}|{tag}")
            
        output_lines.append(" ".join(ttsentence))

    return "\n".join(output_lines)


# --- Botó d'Execució i Sortida ---
if st.button("Etiqueta!", type="primary"):
    with st.spinner('Analitzant el text amb SpaCy...'):
        # IMPORTANT: L'entrada es llegeix del valor actual del widget (input_content)
        result_text = pos_tag_text(input_content) 
        st.session_state['output_text_data'] = result_text

st.subheader("Resultat de l'Etiquetatge")

# Àrea de text de sortida
st.text_area(
    "Text etiquetat:",
    value=st.session_state['output_text_data'],
    height=300,
    # El key="output_text_data" assegura la persistència del resultat
    key="output_text_data", 
    help="Format: FORMA|LEMMA|TAG_COARSE"
)

# --- Descarregar ---
if st.session_state['output_text_data'].strip():
    st.download_button(
        "Descarrega el resultat",
        st.session_state['output_text_data'],
        file_name="tagged_output.txt",
        mime="text/plain"
    )