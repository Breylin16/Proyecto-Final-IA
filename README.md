# VisionAI — Asistente de Descripción Visual

Aplicación de accesibilidad visual que describe escenas para personas con discapacidad visual mediante inteligencia artificial.

## Datos del Estudiante

- **Nombre:** Breylin Gabriel Sanchez Santana
- **Matrícula:** 23-EISN-2-003
- **Asignatura:** Inteligencia Artificial
- **Profesor:** Yoel Pilier
- **Universidad:** O&M

## Descripción del Proyecto

VisionAI permite a una persona con discapacidad visual tomar una foto con su laptop o subir una imagen, y recibir una descripción detallada de la escena en voz alta. La aplicación combina un modelo de Deep Learning local (ResNet18) con una API de visión artificial (Google Gemini) para generar descripciones precisas y naturales en español.

## Arquitectura

El proyecto utiliza una arquitectura híbrida de dos modelos:

1. **ResNet18 (PyTorch local):** Clasifica la imagen localmente en el dispositivo usando un Forward Pass real. Devuelve la categoría más probable entre las 1000 de ImageNet.
2. **Gemini 2.5 Flash (API de nube):** Recibe la imagen original más la clasificación de ResNet18 como contexto, y genera una descripción detallada en español.
3. **Edge TTS:** Convierte la descripción en audio con voz neuronal natural.
4. **Gradio:** Interfaz web accesible con soporte para cámara web, selector de voces y atajos de teclado.

## Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| PyTorch / torchvision | Modelo ResNet18 pre-entrenado para clasificación de imágenes |
| Google Gemini API | Generación de descripciones detalladas de escenas |
| Edge TTS | Síntesis de voz neuronal en español (3 acentos) |
| Gradio | Interfaz gráfica web con componentes de imagen, audio y webcam |
| python-dotenv | Manejo seguro de API keys |

## Características

- Clasificación local de imágenes con Deep Learning (Forward Pass en CPU)
- Descripción detallada de escenas con posiciones, colores y contexto
- Tres voces en español: México, España y Colombia
- Atajos de teclado accesibles (Enter y Barra Espaciadora) con confirmación auditiva
- Imágenes de ejemplo precargadas como respaldo para demos
- Historial de análisis de la sesión
- Indicadores de carga paso a paso (3 fases)
- Manejo de errores con mensajes amigables en español
- API key protegida con .env y .gitignore

## Estructura del Proyecto

```
Proyecto-Final-IA/
├── app.py              # Interfaz principal (Gradio)
├── vision.py           # ResNet18 + Gemini Vision
├── tts.py              # Síntesis de voz (Edge TTS)
├── config.py           # Configuraciones y variables
├── requirements.txt    # Dependencias
├── .env                # API key (no se sube a GitHub)
├── .gitignore          # Archivos excluidos
├── README.md           # Este archivo
└── ejemplos/           # Imágenes de ejemplo
    ├── escritorio.png
    ├── calle.png
    └── cocina.png
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Breylin16/Proyecto-Final-IA.git
cd Proyecto-Final-IA
```

2. Crear entorno virtual e instalar dependencias:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar la API key de Gemini:
```bash
# Crear archivo .env en la raíz del proyecto
GEMINI_API_KEY=tu_api_key_aqui
```

4. Ejecutar la aplicación:
```bash
python app.py
```

La aplicación se abrirá en `http://127.0.0.1:7860`

## Accesibilidad

La aplicación está diseñada para personas con discapacidad visual:

- **Teclas F y J:** Tienen relieves táctiles universales en todos los teclados. La persona coloca sus dedos ahí para orientarse.
- **Enter:** Desde la tecla J, el meñique derecho estira hacia Enter para activar la descripción.
- **Barra Espaciadora:** Como alternativa, el pulgar baja a la Barra Espaciadora.
- **Bip sonoro:** Al presionar Enter o Espacio, se reproduce una confirmación auditiva para que la persona sepa que la acción se ejecutó.
- **Lectores de pantalla:** Gradio genera HTML semántico compatible con NVDA y otros lectores de pantalla.
