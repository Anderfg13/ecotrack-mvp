# EcoTrack MVP

Prototipo de "vibe coding": registra tu huella de carbono diaria
escribiendo una frase en lenguaje natural (ej. *"Hoy comí carne y viajé
20km en bus"*) y obtén un estimado de CO2.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Desplegado en Replit

Importa este repositorio en Replit (o usa el Repl ya creado) — el archivo
`.replit` ya define el comando de arranque (`streamlit run app.py`).

## Configuración del ecosistema de IA

Este laboratorio se desarrolló usando **Claude** como copiloto/orquestador
en lugar de Cursor (equivalencia indicada en el enunciado del laboratorio).
La configuración del entorno de IA quedó documentada en dos archivos
idénticos en contenido:

- [`.cursorrules`](./.cursorrules) — nombre exigido por la rúbrica del
  laboratorio.
- [`CLAUDE.md`](./CLAUDE.md) — nombre que Claude reconoce nativamente como
  archivo de reglas de proyecto.

Ambos definen: el stack permitido (Python + Streamlit, sin frameworks
adicionales), el límite de dependencias (nada de librerías de NLP pesadas
como `nltk` o `fuzzywuzzy` — el parsing es por palabras clave + regex, a
propósito, para mantener el MVP liviano), el estilo de código esperado, y
cómo debía comportarse el agente al recibir instrucciones ambiguas o al
encontrar errores (auto-reparar en vez de pedir depuración manual línea a
línea).

## Decisiones de diseño (arquitectura de intenciones)

Instrucciones estratégicas dadas al agente por componente, y el resultado:

- **Parsing de lenguaje natural** → se pidió detectar comida y transporte
  en una sola frase con múltiples actividades ("comí X y viajé Y"); el
  agente propuso dividir por comas/conectores y priorizar la palabra clave
  más específica (ej. "carne de res" antes que "carne").
- **Factores de emisión** → se pidió usar valores de referencia pública
  (aprox. Our World in Data / DEFRA) en vez de inventarlos, dejando claro
  en el código que son aproximaciones educativas, no certificadas.
- **Manejo de casos sin datos** → se pidió que la app nunca falle en
  silencio: si no detecta comida ni transporte, debe explicar al usuario
  qué tipo de frase espera.
- **Historial de sesión** → se pidió un registro simple del día (sin base
  de datos) para simular el caso de uso real de "huella diaria" sin
  sobre-construir el MVP.

## Archivos clave

- `app.py` — lógica de parsing + interfaz Streamlit.
- `.cursorrules` / `CLAUDE.md` — reglas del agente de IA para este proyecto
  (ver sección "Configuración del ecosistema de IA" arriba).
- `vibe_report.md` — reflexión sobre el proceso de vibe coding.
