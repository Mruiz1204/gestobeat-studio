"""Identidad visual de GestoBeat: índigo de escenario y los colores de nota de los boomwhackers."""

import streamlit as st

NOTAS = {"Do": "#e8413c", "Re": "#f5922f", "Mi": "#f7d23e", "Fa": "#9ccc3c", "Sol": "#2a9d6f", "La": "#8e5cd9"}

# Sonidos de batería en el orden del secuenciador, con el color del gesto que los dispara
SONIDOS = {"Bombo": "#f5922f", "Caja": "#e8413c", "Hi-hat": "#f7d23e", "Aplauso": "#2a9d6f", "Platillo": "#9ccc3c", "Bajo": "#8e5cd9"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Atkinson+Hyperlegible:wght@400;700&display=swap');

:root { --tinta: #1a1838; --escenario: #221f47; --panel: #2a2754; --linea: #3d3970; --texto: #f4f2ff; --suave: #aba6d3; }

html, body, .stApp, [class*="css"], p, li, label, input, textarea, button, .stMarkdown {
  font-family: 'Atkinson Hyperlegible', 'Segoe UI', sans-serif;
}
.stApp { background: var(--tinta); color: var(--texto); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 4rem; }
h1, h2, h3, h4 { font-family: 'Bricolage Grotesque', sans-serif !important; letter-spacing: -0.02em; color: var(--texto) !important; }

/* panel lateral */
section[data-testid="stSidebar"] { background: #15132e; border-right: 1px solid var(--linea); }
section[data-testid="stSidebar"] h3 { font-size: 1.05rem !important; font-weight: 700 !important; margin: 0.6rem 0 0.2rem !important; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label { color: var(--suave) !important; }
section[data-testid="stSidebar"] hr { border-color: var(--linea); margin: 1rem 0; }
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
  background: var(--escenario) !important; color: var(--texto) !important; border: 1px solid var(--linea) !important; border-radius: 12px !important;
}
.stSlider [role="slider"] { background: var(--texto) !important; box-shadow: none !important; }
.stSlider [data-testid="stSliderThumbValue"] { color: var(--texto) !important; font-family: 'Atkinson Hyperlegible', sans-serif; }

/* marca */
.marca { display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap; margin-bottom: 26px; }
.marca .logo { display: flex; align-items: flex-end; gap: 16px; }
.marca .barras { display: flex; align-items: flex-end; gap: 4px; height: 46px; }
.marca .barras i { width: 9px; border-radius: 3px; display: block; }
.marca h1 { font-size: 3.1rem !important; font-weight: 800 !important; line-height: 0.9 !important; margin: 0 !important; padding: 0 !important; }
.marca p { margin: 0; color: var(--suave); max-width: 420px; font-size: 1rem; line-height: 1.45; }

/* sesión */
.sesion { display: grid; grid-template-columns: 1.1fr 1fr; gap: 40px; margin-top: 46px; padding-top: 30px; border-top: 1px solid var(--linea); }
@media (max-width: 780px) { .sesion { grid-template-columns: 1fr; gap: 26px; } .marca h1 { font-size: 2.4rem !important; } }
.sesion h2 { font-size: 1.7rem !important; font-weight: 800 !important; margin: 0 0 8px !important; padding: 0 !important; }
.sesion .resumen { font-size: 1.12rem; color: var(--suave); line-height: 1.55; max-width: 460px; }
.sesion .resumen b { color: var(--texto); }
.hist { display: flex; align-items: flex-end; gap: 10px; min-height: 160px; margin-top: 18px; }
.hist div { flex: 1; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; }
.hist span { width: 100%; border-radius: 10px 10px 4px 4px; min-height: 6px; display: block; }
.hist b { font-family: 'Bricolage Grotesque', sans-serif; font-size: 1rem; margin-top: 6px; }
.hist small { color: var(--suave); font-size: 0.85rem; }
.recientes h3 { font-size: 1.15rem !important; font-weight: 700 !important; margin: 0 0 12px !important; padding: 0 !important; }
.fila { display: flex; align-items: center; gap: 12px; padding: 9px 0; border-bottom: 1px solid var(--linea); font-size: 0.95rem; }
.fila .pt { width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; font-family: 'Bricolage Grotesque', sans-serif;
            font-weight: 800; font-size: 0.78rem; color: #1a1838; flex-shrink: 0; }
.fila .q { color: var(--suave); margin-left: auto; font-size: 0.85rem; }
.vacio-sesion { color: var(--suave); font-size: 1rem; }

/* ayudas */
.ayudas-titulo { font-size: 1.15rem !important; font-weight: 700 !important; margin: 46px 0 12px !important; }
[data-testid="stExpander"] details { background: var(--escenario); border: 1px solid var(--linea) !important; border-radius: 16px; }
[data-testid="stExpander"] summary { font-weight: 700; font-size: 1rem; }
[data-testid="stExpander"] summary:hover { color: #f7d23e; }
[data-testid="stExpander"] li, [data-testid="stExpander"] p { color: #dcd9f2; line-height: 1.6; }
.stMarkdown code { background: var(--panel); color: var(--texto); border-radius: 6px; padding: 1px 6px; }
.pie { margin-top: 40px; color: var(--suave); font-size: 0.85rem; }
</style>
"""


def aplicar():
    st.markdown(CSS, unsafe_allow_html=True)


def marca(descripcion, titulo="GestoBeat"):
    barras = "".join(f'<i style="height:{100 - i * 11}%;background:{c}"></i>' for i, c in enumerate(NOTAS.values()))
    st.markdown(f"""
    <div class="marca">
      <div class="logo"><div class="barras">{barras}</div><h1>{titulo}</h1></div>
      <p>{descripcion}</p>
    </div>""", unsafe_allow_html=True)
