# --- VisionAI: Aplicacion Principal ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
#
# Interfaz grafica en Gradio que integra:
# 1. Analisis de imagen con Google Gemini (deep learning / vision)
# 2. Text-to-Speech con Edge TTS (voz natural en español)
#
# El usuario sube una imagen o usa la camara, la IA describe
# la escena y reproduce la descripcion en voz alta.

import gradio as gr
import os
from PIL import Image
from vision import analizar_imagen
from tts import texto_a_voz
from config import TITULO_APP, DESCRIPCION_APP, VOCES_DISPONIBLES, VOZ_ESPAÑOL

# --- CSS personalizado para un look profesional y accesible ---
CSS_PERSONALIZADO = """
.gradio-container {
    max-width: 1100px !important;
    margin: auto;
}

#titulo-principal {
    text-align: center;
    margin-bottom: 0;
}

#descripcion-app {
    text-align: center;
    opacity: 0.85;
    margin-top: 0;
}

.panel-entrada, .panel-salida {
    border-radius: 12px !important;
}

footer {
    text-align: center;
    opacity: 0.7;
    font-size: 0.85em;
}
"""


def procesar_imagen(imagen, nombre_voz):
    """Funcion principal: recibe imagen, retorna descripcion + audio.

    Pipeline:
    1. Recibe la imagen y la voz desde la interfaz
    2. Envia la imagen a Gemini Vision para obtener descripcion
    3. Convierte la descripcion a voz con Edge TTS
    4. Retorna el texto y el audio al usuario

    Args:
        imagen: PIL.Image - imagen capturada por el usuario
        nombre_voz: str - clave visible seleccionada del dropdown

    Returns:
        tuple: (descripcion_texto, ruta_audio)
    """
    if imagen is None:
        return "No se recibio ninguna imagen. Por favor sube una foto o usa la camara.", None

    try:
        # Notificar visualmente y resolver el acento correspondiente
        gr.Info("Procesando imagen, por favor espera un momento...")
        voz_real = VOCES_DISPONIBLES.get(nombre_voz, VOZ_ESPAÑOL)
        
        # Paso 1: Analizar imagen con Gemini Vision
        descripcion = analizar_imagen(imagen)

        # Paso 2: Convertir descripcion a voz
        archivo_audio = texto_a_voz(descripcion, voz_id=voz_real)

        return descripcion, archivo_audio

    except Exception as e:
        error_tec = str(e)
        print(f"Error interno detectado: {error_tec}")
        
        # Mensajes de estado amigables dependiendo del error
        if "Quota" in error_tec or "429" in error_tec:
            msg = "⚠️ El servicio está saturado en este momento. Por favor, intenta de nuevo en unos minutos."
        elif "API_KEY" in error_tec or "No se encontro" in error_tec:
            msg = "⚠️ Problema de configuración: La clave de Google Gemini no está configurada correctamente."
        elif "WinError" in error_tec or "Connection" in error_tec:
            msg = "⚠️ Hubo un problema de conexión. Por favor, comprueba tu internet y vuelve a intentarlo."
        else:
            msg = "⚠️ Lo siento, ocurrió un error técnico inesperado. Por favor, intenta con otra imagen."
            
        return msg, None


# =============================================================
# INTERFAZ GRADIO
# =============================================================

# Crear la interfaz
with gr.Blocks(
    title=TITULO_APP
) as app:

    # Encabezado centrado y profesional
    gr.Markdown(f"# 👁️ {TITULO_APP}", elem_id="titulo-principal")
    gr.Markdown(DESCRIPCION_APP, elem_id="descripcion-app")

    with gr.Row():
        # Columna izquierda: entrada de imagen
        with gr.Column(scale=1, elem_classes="panel-entrada"):
            gr.Markdown("### 📷 Imagen de entrada")
            imagen_input = gr.Image(
                type="pil",
                label="Sube una imagen o usa la cámara",
                sources=["upload", "webcam"]
            )
            
            # Selector de voces para navegacion de configuracion
            opciones_voces = list(VOCES_DISPONIBLES.keys())
            selector_voz = gr.Dropdown(
                choices=opciones_voces,
                value=opciones_voces[0],
                label="🎙️ Seleccionar Voz / Acento",
                interactive=True
            )
            
            boton_analizar = gr.Button(
                "🔍 Describir escena (O presiona Enter)",
                variant="primary",
                size="lg"
            )

        # Columna derecha: resultados
        with gr.Column(scale=1, elem_classes="panel-salida"):
            gr.Markdown("### 📝 Descripción de la escena")
            texto_output = gr.Textbox(
                label="Descripción generada",
                lines=10,
                interactive=False
            )
            gr.Markdown("### 🔊 Audio de la descripción")
            audio_output = gr.Audio(
                label="Reproducir descripción",
                type="filepath",
                autoplay=True
            )

    # --- Imagenes de ejemplo (backup para la demo del 9 de abril) ---
    ruta_ejemplos = os.path.join(os.path.dirname(__file__), "ejemplos")
    if os.path.exists(ruta_ejemplos):
        gr.Markdown("### 🖼️ Imágenes de ejemplo (haz clic para probar)")
        gr.Examples(
            examples=[
                [os.path.join(ruta_ejemplos, "escritorio.png"), opciones_voces[0]],
                [os.path.join(ruta_ejemplos, "calle.png"), opciones_voces[0]],
                [os.path.join(ruta_ejemplos, "cocina.png"), opciones_voces[0]],
            ],
            inputs=[imagen_input, selector_voz],
            label="Ejemplos precargados"
        )

    # Conectar boton con funcion (ahora pasa la imagen y el dropdown de la voz)
    boton_analizar.click(
        fn=procesar_imagen,
        inputs=[imagen_input, selector_voz],
        outputs=[texto_output, audio_output]
    )

    # ================= Accesibilidad Global =================
    # JavaScript: Escucha el teclado para Discapacidad Visual
    js_accesibilidad = """
    function() {
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                const btn = document.querySelector('button.primary');
                if (btn) {
                    try {
                        let ac = new (window.AudioContext || window.webkitAudioContext)();
                        let osc = ac.createOscillator();
                        let gain = ac.createGain();
                        osc.connect(gain);
                        gain.connect(ac.destination);
                        osc.frequency.value = 800;
                        gain.gain.value = 0.1;
                        osc.start();
                        osc.stop(ac.currentTime + 0.1);
                    } catch(e) {}
                    btn.click();
                }
            }
        });
    }
    """

    # Pie de pagina
    gr.Markdown("---")
    gr.Markdown(
        "**VisionAI** — Proyecto Final de Inteligencia Artificial | "
        "Breylin Gabriel Sanchez Santana | 23-EISN-2-003"
    )


# Ejecutar la aplicacion
if __name__ == "__main__":
    app.launch(
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="sky",
            neutral_hue="slate",
            font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
        ),
        css=CSS_PERSONALIZADO,
        js=js_accesibilidad
    )
