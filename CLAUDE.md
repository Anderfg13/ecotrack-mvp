# CLAUDE.md — Reglas del agente para EcoTrack

> Este archivo cumple, dentro del flujo de trabajo con Claude, el mismo rol
> que `.cursorrules` cumple en Cursor: define la "personalidad" y las
> reglas que la IA debe seguir al trabajar en este proyecto.

## Visión del producto

EcoTrack es un MVP que permite a un usuario registrar su huella de carbono
diaria escribiendo una frase en lenguaje natural (ej. *"Hoy comí carne y
viajé 20km en bus"*), y recibir un estimado de CO2 asociado. Prioriza la
velocidad de validación de la idea sobre la robustez de producción.

## Stack y convenciones técnicas

- **Lenguaje/framework:** Python 3 + Streamlit. No introducir otro framework
  web (Flask, FastAPI, Next.js, etc.) sin que se pida explícitamente.
- **Dependencias:** mínimas. Antes de añadir una librería nueva, preguntar
  si el problema se puede resolver con la librería estándar o con lo que
  ya está instalado.
- **Estructura:** todo el MVP vive en `app.py`. No fragmentar en múltiples
  módulos/carpetas mientras el proyecto siga siendo un prototipo de una
  sola pantalla — evitar sobre-ingeniería.
- **Estilo de código:** limpio, modular en funciones pequeñas y con
  responsabilidad única (parsing, cálculo, UI separados), tipado con
  type hints, nombres de variables en español para el dominio del negocio
  (ej. `FOOD_FACTORS_KG_CO2E_PER_PORCION`) y en inglés para utilidades
  genéricas si aplica.
- **Comentarios:** breves, en español, explicando el *porqué* (ej. de dónde
  salen los factores de emisión), no el *qué* obvio del código.
- **Sin lógica innecesaria:** no agregar autenticación, base de datos,
  persistencia externa ni features fuera del alcance del MVP a menos que
  se pida explícitamente.

## Cómo debe comportarse el agente

1. **Priorizar el "vibe" sobre la sintaxis.** El desarrollador describe la
   intención (qué debe hacer la app, cómo se debe sentir usarla) y el
   agente decide la implementación concreta.
2. **Auto-reparar errores.** Si un cambio rompe la app, el agente debe leer
   el error/traceback y proponer la corrección directamente, sin pedir al
   desarrollador que depure el código línea por línea.
3. **Explicar decisiones de arquitectura en una línea**, no en ensayos:
   el desarrollador quiere contexto suficiente para confiar en la
   decisión, no un tutorial.
4. **Preguntar antes de asumir alcance** cuando una instrucción sea
   ambigua (ej. "agrega más categorías" → ¿de comida, de transporte,
   ambas?), en vez de expandir el MVP sin confirmar.
5. **Probar antes de entregar.** Cada cambio funcional debe validarse
   (casos de prueba manuales o smoke test de que la app arranca) antes de
   darse por terminado.

## Fuera de alcance (por ahora)

- Autenticación de usuarios.
- Persistencia de datos entre sesiones (el historial vive solo en la
  sesión de Streamlit).
- Cálculos de CO2 certificados científicamente — los factores usados son
  aproximaciones públicas de referencia para fines educativos.
