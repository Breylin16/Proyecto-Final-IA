# --- VisionAI: Modulo de Vision ---
# Nombre: Breylin Gabriel Sanchez Santana
# Matricula: 23-EISN-2-003
#
# Este modulo se encarga de analizar imagenes usando la API de Google Gemini.
# Tambien implementa un modelo de PyTorch local (ResNet18) para cumplir con
# los requisitos estrictos de integracion de Deep Learning.

import google.generativeai as genai
from PIL import Image
import torch
import torchvision.models as models
from config import GEMINI_API_KEY


def predecir_con_resnet18(imagen_pil):
    """
    Usa un modelo CNN pre-entrenado (ResNet18) en PyTorch para 
    clasificar la imagen localmente. Esto demuestra integración real
    de un modelo de Deep Learning en el dispositivo (forward pass).
    """
    try:
        # Cargar modelo y pesos (ImageNet)
        weights = models.ResNet18_Weights.DEFAULT
        modelo_local = models.resnet18(weights=weights)
        modelo_local.eval()

        # Preprocesamiento oficial del modelo (a Tensores normalizados)
        transformacion = weights.transforms()
        tensor_batch = transformacion(imagen_pil).unsqueeze(0)

        # Inferencia local (Forward Pass)
        with torch.no_grad():
            prediccion = modelo_local(tensor_batch).squeeze(0).softmax(0)
        
        # Extraer la categoria ganadora (Ej. 'golden retriever')
        id_clase = prediccion.argmax().item()
        categoria_detectada = weights.meta["categories"][id_clase]
        
        return categoria_detectada
    except Exception as e:
        print(f"Advertencia (PyTorch local falló): {e}")
        return None


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

    Usa un modelo local PyTorch (ResNet18) para una inferencia inicial,
    y luego usa el modelo Gemini (API) para generar la descripcion completa.
    """
    configurar_gemini()

    # 1. Ejecutar el modelo PyTorch local para obtener contexto base
    categoria_resnet = predecir_con_resnet18(imagen)
    
    if categoria_resnet:
        contexto_pytorch = f"Mi modelo neuronal local (ResNet18 de PyTorch) ha detectado preliminarmente un objeto clasificado como: '{categoria_resnet}'."
    else:
        contexto_pytorch = ""

    # 2. Usar modelo Gemini con vision para el contexto complejo
    modelo = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt combinado (ResNet18 + Gemini)
    prompt = f"""Eres un asistente de accesibilidad visual para personas con discapacidad visual.

{contexto_pytorch}
Usa ese dato como pista, pero enfócate en analizar y describir la imagen completa de forma muy detallada y clara en español.
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

    # Enviar imagen y prompt al modelo
    respuesta = modelo.generate_content([prompt, imagen])

    return respuesta.text
