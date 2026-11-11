"""
GestoBeat Studio — Miguel Ruiz
Proyecto final · Creación de Interfaces Multimodales (EAFIT 2026-2)

Versión de beats de GestoBeat: cada gesto de la mano dispara un sonido de batería, lo que tocas
se graba en un loop de un compás (16 pasos, cuantizado al tiempo) y le vas sumando capas.
Con la voz se controla el estudio (grabar, parar, tempo) y un ESP32 en Wokwi parpadea al ritmo.

Todo lo que necesita tiempo real (cámara, detector de mano o modelo de Teachable Machine,
sonido, loop, voz y MQTT) corre en el navegador, dentro del componente de `componente/`.
"""

from collections import Counter
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from estilo import SONIDOS, aplicar, marca

st.set_page_config(page_title="GestoBeat Studio", page_icon="🥁", layout="wide", initial_sidebar_state="collapsed")
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
    bpm = st.slider("BPM al abrir", 60, 160, 90, 5, help="Luego lo cambias en el estudio con − y +, o con la voz.")
    st.divider()
    st.markdown("### Conexión con el ESP32")
    broker = st.text_input("Broker MQTT (websocket)", value="wss://broker.hivemq.com:8884/mqtt",
                           help="El navegador entra por websocket seguro; el ESP32 de Wokwi usa el mismo broker por el puerto 1883.")
    topico = st.text_input("Tópico", value="gestobeat_miguelruiz",
                           help="El mismo tópico del ESP32 de GestoBeat: cada golpe enciende el LED de su gesto.")

# ─────────────────────────────────────────────
# ESTUDIO
# ─────────────────────────────────────────────
marca("Arma un beat con las manos: cada gesto es un sonido de batería, lo que tocas se repite en loop y le vas sumando capas.",
      titulo="GestoBeat Studio")

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
    if estado.get("pasos"):
        frase += f" Tu beat tiene <b>{estado['pasos']} golpes</b> en el compás y va a <b>{estado.get('bpm', 90)} BPM</b>."
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

with st.expander("Cómo se arma un beat"):
    st.markdown(f"""
1. **Prueba los sonidos.** Toca los pads, usa las teclas 1 a 6 o enciende la cámara y haz los gestos:
   ✊ bombo, ✋ caja, ☝️ hi-hat, ✌️ aplauso, 🤟 platillo (pulgar, índice y meñique) y 👍 bajo.
2. **Dale ▶** para que corra el loop y escucha el metrónomo: cuatro tiempos por compás.
3. **Dale Grabar** (o la tecla R) y toca encima. Cada golpe se acomoda solo al tiempo más cercano, aunque llegues un poco tarde.
4. **Suma capas:** primero el bombo, después la caja, después el hi-hat y al final el bajo.
5. **Corrige en la grilla:** toca una casilla para poner o quitar un golpe, o la × de una fila para borrarla.
6. ¿Sin ideas? Carga un patrón de ejemplo (*Hip hop*, *Reggaetón* o *Rock*) y grábale encima.
""")

with st.expander("Comandos de voz"):
    st.markdown("""
- «**grabar**», «**parar**», «**tocar**» o «**dale**»
- «**más rápido**», «**más lento**» o un número, como «**ciento veinte**»
- «**borrar**», «**metrónomo**»
- «**hip hop**», «**reggaetón**», «**rock**» para cargar un patrón
- El nombre de un sonido, como «**bombo**» o «**platillo**», para tocarlo
""")

with st.expander("Conectar el ESP32 en Wokwi"):
    st.markdown(f"""
Usa el mismo proyecto de Wokwi de GestoBeat: cada golpe enciende el LED del color de su gesto y suena en el buzzer,
así las luces siguen el ritmo del loop. El tópico tiene que ser `{topico}`.
""")

st.markdown('<p class="pie">GestoBeat Studio es la versión de beats del proyecto final de Miguel Ruiz para Creación de Interfaces Multimodales, EAFIT 2026-2.</p>',
            unsafe_allow_html=True)
