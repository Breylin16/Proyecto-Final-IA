# --- VisionAI: Modulo de Voz (TTS) ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
#
# Este modulo convierte texto a voz usando Edge TTS de Microsoft.
# Es gratuito y no requiere API key.
# Las voces son neuronales y suenan naturales en español.

import edge_tts
import asyncio
import tempfile
import os
from config import VOZ_ESPAÑOL, VOZ_VELOCIDAD, VOZ_TONO, VOZ_VOLUMEN


async def _generar_audio_async(texto, archivo_salida):
    """Genera audio a partir de texto usando Edge TTS (asincrono).

    Args:
        texto: str - el texto a convertir en voz
        archivo_salida: str - ruta donde guardar el archivo de audio

    Returns:
        str - ruta al archivo de audio generado
    """
    communicate = edge_tts.Communicate(
        text=texto,
        voice=VOZ_ESPAÑOL,
        rate=VOZ_VELOCIDAD,
        volume=VOZ_VOLUMEN,
        pitch=VOZ_TONO
    )
    await communicate.save(archivo_salida)
    return archivo_salida


def texto_a_voz(texto):
    """Convierte texto a un archivo de audio MP3.

    Usa Edge TTS (Microsoft) para generar voz natural en español.
    El archivo se guarda en una carpeta temporal del sistema.

    Args:
        texto: str - la descripcion a convertir en voz

    Returns:
        str - ruta al archivo MP3 generado
    """
    # Crear archivo temporal para el audio
    archivo_temp = tempfile.NamedTemporaryFile(
        suffix=".mp3", delete=False, dir=tempfile.gettempdir()
    )
    archivo_salida = archivo_temp.name
    archivo_temp.close()

    # Ejecutar la generacion de audio
    # Nota: se usa new_event_loop() en vez de asyncio.run() porque
    # Gradio ya tiene un event loop corriendo en Windows y asyncio.run()
    # lanzaria un error "cannot run nested event loop".
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_generar_audio_async(texto, archivo_salida))
    finally:
        loop.close()

    return archivo_salida
