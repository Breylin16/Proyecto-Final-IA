# --- VisionAI: Asistente de Descripcion Visual ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
# Proyecto Final de Inteligencia Artificial
#
# Este archivo contiene la configuracion general del proyecto.
# Las API keys y parametros se definen aqui para facilitar su uso.

import os

# --- CONFIGURACION DE API ---
# La API key de Google Gemini se lee de una variable de entorno
# para no exponer credenciales en el codigo fuente.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- CONFIGURACION DE VOZ (TTS) ---
# Edge TTS permite usar voces de Microsoft de forma gratuita
# Lista de voces en español disponibles:
VOZ_ESPAÑOL = "es-MX-DaliaNeural"  # Voz femenina mexicana (clara y natural)
VOZ_VELOCIDAD = "+0%"               # Velocidad normal

# --- CONFIGURACION DE LA APLICACION ---
TITULO_APP = "VisionAI — Asistente de Descripción Visual"
DESCRIPCION_APP = """
Aplicación de accesibilidad visual que describe escenas para personas con discapacidad visual.
Sube una imagen o usa la cámara → la IA describe lo que ve → lo reproduce en voz alta.
"""
