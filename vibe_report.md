# Vibe Report — EcoTrack MVP

*(Nota: en mi flujo usé Claude como copiloto/orquestador en lugar de
Cursor, con `CLAUDE.md` cumpliendo el rol de `.cursorrules`, y Replit
como entorno de despliegue rápido.)*

## Cómo configuré las reglas de mi agente

Antes de pedir una sola línea de código, escribí `CLAUDE.md` con la visión
del producto, el stack (Python + Streamlit), y restricciones explícitas:
nada de dependencias innecesarias, todo en un solo archivo mientras siga
siendo un prototipo, funciones pequeñas y con una responsabilidad clara,
y —lo más importante— que el agente pruebe cada cambio antes de darlo por
terminado. Definir esto primero cambió la calidad de las respuestas: en
vez de recibir código genérico, recibí decisiones ya alineadas con el
"vibe" que quería para EcoTrack (rápido de iterar, sin sobre-ingeniería).

## Dificultades al delegar código a la IA

La principal dificultad no fue técnica sino de *especificación*. Pedir
"que calcule el CO2 de lo que escriba el usuario" es ambiguo: ¿qué pasa si
la frase no tiene ni comida ni transporte? ¿Cómo se separan varias
actividades en una sola oración? Tuve que iterar la instrucción original
en reglas concretas (separar por comas/conectores, usar la palabra clave
más específica primero, no fallar silenciosamente si no detecta nada) para
que el resultado fuera predecible. También noté que confiar ciegamente en
el primer resultado es arriesgado: probé el ejemplo exacto del enunciado
("Hoy comí carne y viajé 20km en bus") y solo verificando el cálculo a
mano confirmé que el estimado (8.39 kg CO2e) tenía sentido. Delegar no
significa dejar de verificar.

## De "escribir código" a "orquestar una visión"

Se siente como un cambio de rol más que de herramienta: pasé de pensar en
sintaxis (¿cómo separo esta cadena en Python?) a pensar en producto (¿qué
necesita sentir el usuario cuando escribe su día y ve el resultado?). Es
liberador porque el tiempo se va en decisiones de diseño y validación, no
en teclear boilerplate. Pero también exige una disciplina distinta: hay
que ser explícito sobre el alcance (si no defines límites, la IA puede
sobre-construir), y hay que revisar el resultado con ojo crítico, porque
la velocidad de generación no reemplaza la responsabilidad de entender lo
que se está desplegando. En resumen: orquestar se siente menos como
"programar" y más como dirigir — se gana velocidad, se pierde el control
línea a línea, y ese intercambio solo vale la pena si uno mantiene la
supervisión activa sobre el resultado final.
