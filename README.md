# 🥁 Tu primer beat (GestoBeat Studio) · Miguel Ruiz

Versión de aprendizaje del proyecto final de **Creación de Interfaces Multimodales** (EAFIT 2026-2).

Un juego para aprender a hacer un beat con las manos, en cuatro lecciones: el bombo ✊ en el 1 y el 3, la caja ✋ en el 2 y el 4, el hi-hat ☝️ en los «y» y todo junto. Cada lección toca un compás de ejemplo y luego le dice al jugador si llegó a tiempo. La voz controla las lecciones y el ESP32 de Wokwi parpadea al ritmo.

| Gesto | Nota | LED |
|---|---|---|
| ✋ mano abierta | Do | rojo (GPIO 13) |
| ✊ puño | Re | naranja (GPIO 12) |
| ☝️ un dedo | Mi | amarillo (GPIO 14) |
| 🤟 pulgar, índice y meñique | Fa | verde limón (GPIO 33) |
| ✌️ dos dedos | Sol | verde (GPIO 27) |
| 👍 pulgar arriba | La | morado (GPIO 26) |

## Modalidades

| Modalidad | Tipo | Tecnología |
|---|---|---|
| Gestos de la mano | Entrada | Detector de mano MediaPipe Hands (21 puntos, cuenta los dedos) o el modelo de Teachable Machine con TensorFlow.js |
| Tablero y teclado | Entrada | Barras táctiles y teclas 1–6 |
| Voz | Entrada | Web Speech API («piano», «guitarra», «marimba», «juego», «escuchar», «do re mi»…) |
| Sonido | Salida | Tone.js, escala de Do (Do, Re, Mi, Fa, Sol, La) |
| Pantalla | Salida | Streamlit + componente propio |
| Luces y buzzer | Salida | ESP32 en Wokwi por MQTT (`{"nota": "Mi", "instrumento": "piano"}`) |

## Estructura

- `Inicio.py`: la app de Streamlit (panel lateral, resumen de la sesión, ayudas).
- `componente/index.html`: el instrumento. Cámara, modelo, sonido, voz y MQTT corren en el navegador para que la música no se corte.
- `componente/lib/`: TensorFlow.js, MediaPipe Hands, Tone.js y mqtt.js incluidos en el repositorio.
- `wokwi/`: `sketch.ino`, `diagram.json` y `libraries.txt` del ESP32.

## Desplegar

Streamlit Cloud → *Create app* → repositorio `Mruiz1204/gestobeat-studio`, rama `main`, archivo `Inicio.py`.
