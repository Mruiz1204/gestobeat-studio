"""
Tu primer beat (GestoBeat Studio) — Miguel Ruiz
Proyecto final · Creación de Interfaces Multimodales (EAFIT 2026-2)

Juego para aprender a hacer un beat con las manos: cada gesto es un sonido de batería y en cuatro
lecciones se arma el ritmo más básico (bombo en 1 y 3, caja en 2 y 4, hi-hat en los «y»). La app
toca un compás de ejemplo, escucha al jugador y le dice si llegó a tiempo. La voz controla las
lecciones y un ESP32 en Wokwi parpadea al ritmo.

Todo lo que necesita tiempo real (cámara, detector de mano o modelo de Teachable Machine,
sonido, loop, voz y MQTT) corre en el navegador, dentro del componente de `componente/`.
"""

from collections import Counter
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from estilo import SONIDOS, aplicar, marca

st.set_page_config(page_title="Tu primer beat", page_icon="🥁", layout="wide", initial_sidebar_state="collapsed")
aplicar()

_studio = components.declare_component("gestobeat_studio", path=str(Path(__file__).parent / "componente"))

ORIGEN = {"gesto": "con gestos", "pad": "en los pads", "teclado": "con el teclado", "voz": "con la voz"}

# ─────────────────────────────────────────────
# AJUSTES (panel lateral)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Reconocer los gestos")
    forma = st.radio(
        "Cómo reconoce la cámara tus gestos",
        ["Detector de mano", "Mi modelo de Teachable Machine"],
        help="El detector de mano ubica los 21 puntos de tu mano y cuenta los dedos levantados: funciona con "
             "cualquier fondo y luz. El modelo de Teachable Machine usa las fotos con las que lo entrenaste.",
    )
    reconocimiento = "mano" if forma == "Detector de mano" else "modelo"
    modelo_url = st.text_input(
        "Enlace de Teachable Machine",
        value="https://teachablemachine.withgoogle.com/models/0cq29_e5i/",
        placeholder="https://teachablemachine.withgoogle.com/models/…/", disabled=reconocimiento == "mano",
        help="Es el mismo modelo de GestoBeat: las clases Do, Re, Mi, Fa, Sol y La disparan los sonidos de batería.",
    )
    umbral = st.slider("Seguridad del modelo para tocar", 0.5, 0.99, 0.75, 0.01, disabled=reconocimiento == "mano",
                       help="El golpe solo suena si el modelo está así de seguro del gesto.")
    st.divider()
    st.markdown("### Tempo")
    bpm = st.slider("Velocidad de las lecciones (BPM)", 60, 120, 80, 5, help="Más bajo es más fácil. También lo cambias con − y + o diciendo «más lento».")
    st.divider()
    st.markdown("### Conexión con el ESP32")
    broker = st.text_input("Broker MQTT (websocket)", value="wss://broker.hivemq.com:8884/mqtt",
                           help="El navegador entra por websocket seguro; el ESP32 de Wokwi usa el mismo broker por el puerto 1883.")
    topico = st.text_input("Tópico", value="gestobeat_miguelruiz",
                           help="El mismo tópico del ESP32 de GestoBeat: cada golpe enciende el LED de su gesto.")

# ─────────────────────────────────────────────
# ESTUDIO
# ─────────────────────────────────────────────
marca("Aprende a hacer un beat con tus manos: cada gesto es un sonido de batería y en cuatro lecciones armas el ritmo más básico de todos.",
      titulo="Tu primer beat")

estado = _studio(reconocimiento=reconocimiento, modelo_url=modelo_url, umbral=umbral, bpm=bpm,
                 broker=broker, topico=topico, key="studio", default=None) or {}

# ─────────────────────────────────────────────
# TU SESIÓN (lo envía el componente)
# ─────────────────────────────────────────────
por_sonido = Counter(estado.get("por_sonido", {}))
por_origen = Counter(estado.get("por_origen", {}))
total = estado.get("golpes", 0)

if total:
    favorito = por_sonido.most_common(1)[0][0]
    forma = ORIGEN.get(por_origen.most_common(1)[0][0], "")
    frase = (f"Llevas <b>{total} {'golpe' if total == 1 else 'golpes'}</b>, casi todos {forma}. "
             f"El que más suena es el <b style='color:{SONIDOS.get(favorito, '#fff')}'>{favorito.lower()}</b>.")
    if estado.get("primer_beat"):
        frase += " <b>Ya hiciste tu primer beat.</b>"
    elif estado.get("lecciones"):
        frase += f" Vas en la lección <b>{estado['lecciones'] + 1} de 4</b>."

    if estado.get("mqtt_enviados"):
        frase += f" El ESP32 recibió <b>{estado['mqtt_enviados']}</b> mensajes."
    maximo = max(por_sonido.values())
    hist = "".join(
        f'<div><span style="height:{max(por_sonido.get(n, 0) / maximo * 110, 6):.0f}px;background:{c}"></span>'
        f'<b style="color:{c}">{n}</b><small>{por_sonido.get(n, 0)}</small></div>'
        for n, c in SONIDOS.items()
    )
    filas = "".join(
        f'<div class="fila"><span class="pt" style="background:{SONIDOS.get(u["sonido"], "#fff")}">{u["sonido"][:2]}</span>'
        f'<span>{u["sonido"]}, {ORIGEN.get(u["origen"], u["origen"])}</span><span class="q">{u["hora"]}</span></div>'
        for u in estado.get("ultimas", [])[:6]
    )
    st.markdown(f"""
    <div class="sesion">
      <div><h2>Tu sesión</h2><div class="resumen">{frase}</div><div class="hist">{hist}</div></div>
      <div class="recientes"><h3>Lo último que tocaste</h3>{filas}</div>
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="sesion">
      <div><h2>Tu sesión</h2><p class="vacio-sesion">Cuando empieces a tocar, aquí vas a ver cuántos golpes llevas, cuál suena más y cómo va tu beat.</p></div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AYUDAS
# ─────────────────────────────────────────────
st.markdown('<h3 class="ayudas-titulo">Antes de tocar</h3>', unsafe_allow_html=True)

with st.expander("Cómo funcionan las 4 lecciones"):
    st.markdown("""
1. **El bombo** ✊ en el 1 y el 3: el latido del beat.
2. **La caja** ✋ en el 2 y el 4: le responde al bombo.
3. **El hi-hat** ☝️ en los «y», entre cada tiempo. Con la cámara basta con **mantener** ☝️ y se toca solo.
4. **Todo junto:** tocas tú el bombo y la caja alternando ✊ y ✋ encima del hi-hat.

Cada lección empieza con un compás de ejemplo; luego es tu turno y la app te dice si llegaste **a tiempo**, **un poco antes**
o **un poco tarde**. La cuenta «1 y 2 y 3 y 4 y» marca de color dónde va cada golpe. Al terminar, el beat queda sonando para que le toques encima aplausos ✌️, platillo 🤟 o bajo 👍.
""")

with st.expander("Comandos de voz"):
    st.markdown("""
- «**empezar**» para arrancar la lección, «**escuchar**» para oír otra vez el ejemplo, «**saltar**» para pasar a la siguiente
- «**más lento**» o «**más rápido**», o un número, como «**ochenta**»
- «**parar**» y «**dale**» para detener o seguir
- El nombre de un sonido, como «**bombo**» o «**caja**», para tocarlo
""")

with st.expander("Conectar el ESP32 en Wokwi"):
    st.markdown(f"""
Usa el mismo proyecto de Wokwi de GestoBeat: cada golpe enciende el LED del color de su gesto y suena en el buzzer,
así las luces siguen el ritmo del loop. El tópico tiene que ser `{topico}`.
""")

st.markdown('<p class="pie">Tu primer beat es la versión de aprendizaje del proyecto final de Miguel Ruiz para Creación de Interfaces Multimodales, EAFIT 2026-2.</p>',
            unsafe_allow_html=True)
