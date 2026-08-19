"""
EcoTrack MVP - Registro de huella de carbono diaria en lenguaje natural.

El usuario escribe una frase como:
  "Hoy comí carne y viajé 20km en bus"
y la app estima las emisiones de CO2 asociadas.

Enfoque intencionalmente simple (vibe coding / MVP): parsing por palabras
clave y expresiones regulares, sin dependencias de NLP pesadas.
"""

import re
from datetime import datetime

import streamlit as st

# ---------------------------------------------------------------------------
# Factores de emisión (kg CO2e). Valores aproximados de referencia pública
# (Our World in Data / DEFRA) para un MVP educativo, no para uso científico.
# ---------------------------------------------------------------------------

FOOD_FACTORS_KG_CO2E_PER_PORCION = {
    "carne de res": 6.61,
    "carne": 6.61,
    "res": 6.61,
    "hamburguesa": 6.61,
    "cordero": 6.61,
    "cerdo": 3.72,
    "pollo": 1.10,
    "pavo": 1.10,
    "pescado": 1.85,
    "atún": 1.85,
    "atun": 1.85,
    "mariscos": 2.60,
    "huevo": 0.45,
    "huevos": 0.45,
    "queso": 1.00,
    "lácteos": 1.00,
    "lacteos": 1.00,
    "leche": 0.60,
    "vegetariano": 0.50,
    "vegetariana": 0.50,
    "vegano": 0.30,
    "vegana": 0.30,
    "verduras": 0.30,
    "ensalada": 0.30,
    "fruta": 0.20,
}

TRANSPORT_FACTORS_KG_CO2E_PER_KM = {
    "avión": 0.255,
    "avion": 0.255,
    "vuelo": 0.255,
    "carro": 0.192,
    "auto": 0.192,
    "coche": 0.192,
    "taxi": 0.192,
    "uber": 0.192,
    "moto": 0.113,
    "motocicleta": 0.113,
    "bus": 0.089,
    "autobús": 0.089,
    "autobus": 0.089,
    "buseta": 0.089,
    "tren": 0.041,
    "metro": 0.041,
    "bicicleta": 0.0,
    "bici": 0.0,
    "caminar": 0.0,
    "caminando": 0.0,
    "a pie": 0.0,
}

KM_PATTERN = re.compile(r"(\d+(?:[.,]\d+)?)\s*km")


def _split_clauses(text: str) -> list[str]:
    """Divide la frase en actividades separadas por comas o conectores."""
    parts = re.split(r",| y | además | tambi[eé]n ", text.lower())
    return [p.strip() for p in parts if p.strip()]


def _match_keyword(clause: str, factors: dict) -> str | None:
    """Devuelve la palabra clave más específica (más larga) que aparece en la frase."""
    for keyword in sorted(factors, key=len, reverse=True):
        if re.search(r"\b" + re.escape(keyword) + r"\b", clause):
            return keyword
    return None


def analyze(text: str) -> tuple[list[dict], float]:
    """Analiza una frase en lenguaje natural y estima el CO2 generado.

    Devuelve una lista de actividades detectadas y el total en kg CO2e.
    """
    results = []
    total = 0.0

    for clause in _split_clauses(text):
        food = _match_keyword(clause, FOOD_FACTORS_KG_CO2E_PER_PORCION)
        if food:
            factor = FOOD_FACTORS_KG_CO2E_PER_PORCION[food]
            total += factor
            results.append({
                "tipo": "🍽️ Alimentación",
                "detalle": food,
                "co2": factor,
            })
            continue

        transport = _match_keyword(clause, TRANSPORT_FACTORS_KG_CO2E_PER_KM)
        if transport:
            km_match = KM_PATTERN.search(clause)
            km = float(km_match.group(1).replace(",", ".")) if km_match else 0.0
            factor = TRANSPORT_FACTORS_KG_CO2E_PER_KM[transport] * km
            total += factor
            detalle = f"{transport} ({km:g} km)" if km_match else f"{transport} (sin distancia)"
            results.append({
                "tipo": "🚌 Transporte",
                "detalle": detalle,
                "co2": factor,
            })

    return results, total


# ---------------------------------------------------------------------------
# Interfaz Streamlit
# ---------------------------------------------------------------------------

st.set_page_config(page_title="EcoTrack", page_icon="🌱", layout="centered")

if "log" not in st.session_state:
    st.session_state.log = []  # lista de {"hora", "texto", "co2"}

st.title("🌱 EcoTrack")
st.caption("Registra tu día en lenguaje natural y estima tu huella de carbono.")

texto = st.text_area(
    "¿Qué hiciste hoy?",
    placeholder="Ej: Hoy comí carne y viajé 20km en bus",
    height=90,
)

col1, col2 = st.columns([1, 1])
calcular = col1.button("Calcular huella 🌍", type="primary")
limpiar = col2.button("Borrar historial")

if limpiar:
    st.session_state.log = []
    st.rerun()

if calcular and texto.strip():
    actividades, total = analyze(texto)

    if not actividades:
        st.warning(
            "No detecté alimentación ni transporte en esa frase. "
            "Prueba mencionar comida (ej. 'carne', 'pollo') o transporte con distancia "
            "(ej. '20km en bus')."
        )
    else:
        st.subheader(f"Estimado: {total:.2f} kg CO2e")
        for actividad in actividades:
            st.write(f"{actividad['tipo']} — {actividad['detalle']}: **{actividad['co2']:.2f} kg CO2e**")

        st.session_state.log.append({
            "hora": datetime.now().strftime("%H:%M"),
            "texto": texto.strip(),
            "co2": round(total, 2),
        })

if st.session_state.log:
    st.divider()
    st.subheader("📋 Historial de hoy")
    dia_total = sum(item["co2"] for item in st.session_state.log)
    st.metric("Total acumulado hoy", f"{dia_total:.2f} kg CO2e")
    st.dataframe(
        st.session_state.log[::-1],
        column_config={
            "hora": "Hora",
            "texto": "Actividad",
            "co2": "kg CO2e",
        },
        hide_index=True,
        use_container_width=True,
    )
    st.bar_chart(
        {item["hora"]: item["co2"] for item in st.session_state.log},
    )
