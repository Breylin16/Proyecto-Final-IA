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
from PIL import Image
from vision import analizar_imagen
from tts import texto_a_voz
from config import TITULO_APP, DESCRIPCION_APP


def procesar_imagen(imagen):
    """Funcion principal: recibe imagen, retorna descripcion + audio.

    Pipeline:
    1. Recibe la imagen del usuario (upload o camara)
    2. Envia la imagen a Gemini Vision para obtener descripcion
    3. Convierte la descripcion a voz con Edge TTS
    4. Retorna el texto y el audio al usuario

    Args:
        imagen: PIL.Image - imagen capturada por el usuario

    Returns:
        tuple: (descripcion_texto, ruta_audio)
    """
    if imagen is None:
        return "No se recibio ninguna imagen. Por favor sube una foto o usa la camara.", None

    try:
        # Paso 1: Analizar imagen con Gemini Vision
        descripcion = analizar_imagen(imagen)

        # Paso 2: Convertir descripcion a voz
        archivo_audio = texto_a_voz(descripcion)

        return descripcion, archivo_audio

    except Exception as e:
        error_msg = f"Error al procesar la imagen: {str(e)}"
        return error_msg, None


# =============================================================
# INTERFAZ GRADIO
# =============================================================

# Crear la interfaz
with gr.Blocks(
    title=TITULO_APP,
    theme=gr.themes.Soft()
) as app:

    # Encabezado
    gr.Markdown(f"# 👁️ {TITULO_APP}")
    gr.Markdown(DESCRIPCION_APP)

    with gr.Row():
        # Columna izquierda: entrada de imagen
        with gr.Column(scale=1):
            gr.Markdown("### 📷 Imagen de entrada")
            imagen_input = gr.Image(
                type="pil",
                label="Sube una imagen o usa la camara",
                sources=["upload", "webcam"]
            )
            boton_analizar = gr.Button(
                "🔍 Describir escena",
                variant="primary",
                size="lg"
            )

        # Columna derecha: resultados
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Descripcion de la escena")
            texto_output = gr.Textbox(
                label="Descripcion generada",
                lines=10,
                interactive=False
            )
            gr.Markdown("### 🔊 Audio de la descripcion")
            audio_output = gr.Audio(
                label="Reproducir descripcion",
                type="filepath",
                autoplay=True
            )

    # Conectar boton con funcion
    boton_analizar.click(
        fn=procesar_imagen,
        inputs=[imagen_input],
        outputs=[texto_output, audio_output]
    )

    # Pie de pagina
    gr.Markdown("---")
    gr.Markdown(
        "**VisionAI** — Proyecto Final de Inteligencia Artificial | "
        "Breylin Gabriel Sanchez Santana | 23-EISN-2-003"
    )


# Ejecutar la aplicacion
if __name__ == "__main__":
    app.launch()
