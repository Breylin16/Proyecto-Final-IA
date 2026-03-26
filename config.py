# --- VisionAI: Asistente de Descripcion Visual ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
# Proyecto Final de Inteligencia Artificial
#
# Este archivo contiene la configuracion general del proyecto.
# Las API keys y parametros se definen aqui para facilitar su uso.

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# --- CONFIGURACION DE API ---
# La API key de Google Gemini se lee de una variable de entorno
# para no exponer credenciales en el codigo fuente.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- CONFIGURACION DE VOZ (TTS) ---
# Edge TTS permite usar voces de Microsoft de forma gratuita
# Lista de voces en español disponibles:
VOCES_DISPONIBLES = {
    "🇲🇽 Dalia (México) - Femenina clara": "es-MX-DaliaNeural",
    "🇪🇸 Elvira (España) - Femenina formal": "es-ES-ElviraNeural",
    "🇨🇴 Salome (Colombia) - Femenina cálida": "es-CO-SalomeNeural"
}
VOZ_ESPAÑOL = VOCES_DISPONIBLES["🇲🇽 Dalia (México) - Femenina clara"] # Voz por defecto
VOZ_VELOCIDAD = "+0%"               # Velocidad normal (+5% más rápido, -5% más lento)
VOZ_TONO = "+0Hz"                   # Tono de la voz (ajuste fino en Hz para mayor realismo)
VOZ_VOLUMEN = "+0%"                 # Volumen base

# --- CONFIGURACION DE LA APLICACION ---
TITULO_APP = "VisionAI — Asistente de Descripción Visual"
DESCRIPCION_APP = """
Aplicación de accesibilidad visual que describe escenas para personas con discapacidad visual.
Sube una imagen o usa la cámara → la IA describe lo que ve → lo reproduce en voz alta.
"""
