# --- VisionAI: Modulo de Vision ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
#
# Este modulo se encarga de analizar imagenes usando la API de Google Gemini.
# Recibe una imagen y retorna una descripcion detallada de la escena.

import google.generativeai as genai
from PIL import Image
from config import GEMINI_API_KEY


def configurar_gemini():
    """Configura la API de Google Gemini con la key del entorno."""
    if not GEMINI_API_KEY:
        raise ValueError(
            "No se encontro GEMINI_API_KEY. "
            "Configura la variable de entorno antes de ejecutar."
        )
    genai.configure(api_key=GEMINI_API_KEY)


def analizar_imagen(imagen):
    """Recibe una imagen (PIL Image) y retorna una descripcion detallada.

    Usa el modelo Gemini con capacidades de vision para generar
    una descripcion completa de la escena en español.

    Args:
        imagen: PIL.Image - la imagen a analizar

    Returns:
        str - descripcion de la escena en español
    """
    configurar_gemini()

    # Usar modelo Gemini con vision
    modelo = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt para que describa como asistente de accesibilidad
    prompt = """Eres un asistente de accesibilidad visual para personas con discapacidad visual.
Describe esta imagen de forma detallada y clara en español.
Incluye:
- Que objetos, personas o elementos hay en la escena
- Donde estan ubicados (izquierda, derecha, centro, fondo)
- Colores predominantes
- Cualquier texto visible
- El contexto general de la escena

Regla MUY IMPORTANTE: Tu respuesta será leída en voz alta por un sistema TTS. 
NO uses NINGÚN formato Markdown (nada de asteriscos, sin negritas, sin listas con guiones). 
Escribe todo en párrafos de texto plano natural y descriptivo, como si le estuvieras 
contando a alguien que no puede ver lo que hay frente a ellos. Se conciso pero completo."""

    # Enviar imagen al modelo
    respuesta = modelo.generate_content([prompt, imagen])

    return respuesta.text
