# VisionAI — Asistente de Descripción Visual

**Nombre:** Breylin Gabriel Sanchez Santana  
**Matrícula:** 23-EISN-2-003  
**Materia:** Inteligencia Artificial  
**Profesor:** Yoel Pilier

## Descripción

VisionAI es una aplicación de accesibilidad visual que describe escenas para personas con discapacidad visual. El usuario sube una imagen o usa la cámara web, la IA analiza la escena y reproduce una descripción detallada en voz alta.

## Tecnologías

- **PyTorch (ResNet18):** Modelo de Deep Learning local para clasificación preliminar de imágenes
- **Google Gemini:** API de visión artificial para generación de descripciones detalladas
- **Edge TTS:** Síntesis de voz neuronal en español (3 acentos disponibles)
- **Gradio:** Interfaz gráfica web interactiva

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

La aplicación se abrirá en `http://127.0.0.1:7860`
