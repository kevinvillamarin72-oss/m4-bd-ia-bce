"""Flujo de exportaciones: extrae dos fuentes, las une con defensas y guarda el resultado.
Autor: J. Tito · Creado: 2026-10-26 · Fuente: datos de clase (sinteticos)"""
import logging, sys, unicodedata
from datetime import date
import pandas as pd

# ---------- 1 · PARAMETROS (todo lo que puede cambiar, junto y arriba) ----------
RUTA_EXPORTACIONES = "datos/exportaciones.csv"
RUTA_CATALOGO      = "datos/catalogo.csv"
SALIDA             = f"salida/exportaciones_con_codigo_{date.today().isoformat()}.csv"
FILAS_ESPERADAS    = 6
TOTAL_ESPERADO     = 8679.13

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler("flujo.log"), logging.StreamHandler()])
log = logging.getLogger("flujo")

# ---------- 2 · LAS TRES FUNCIONES ----------
def normalizar(texto):
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sin_tildes.strip().lower()

def extraer():
    a = pd.read_csv(RUTA_EXPORTACIONES); b = pd.read_csv(RUTA_CATALOGO, dtype={"codigo": str})
    log.info("extraidas %d filas de exportaciones y %d del catalogo", len(a), len(b))
    return a, b

def transformar(a, b):
    a["clave"] = a["producto"].map(normalizar); b["clave"] = b["producto"].map(normalizar)
    if len(a) != FILAS_ESPERADAS:
        raise ValueError(f"esperaba {FILAS_ESPERADAS} filas y llegaron {len(a)}")
    union = pd.merge(a, b[["clave", "codigo"]], on="clave", how="left",
                     validate="one_to_one", indicator=True)
    sin_cruzar = union[union["_merge"] != "both"]
    if len(sin_cruzar):
        log.warning("%d filas sin codigo: %s", len(sin_cruzar), list(sin_cruzar["producto"]))
    total = round(union["monto_mm_usd"].sum(), 2)
    if abs(total - TOTAL_ESPERADO) > 0.01:
        raise ValueError(f"el total cambio: esperaba {TOTAL_ESPERADO} y salio {total}")
    return union.drop(columns=["clave", "_merge"])

def cargar(tabla):
    import os; os.makedirs("salida", exist_ok=True)
    tabla.to_csv(SALIDA, index=False); log.info("guardado %s (%d filas)", SALIDA, len(tabla))

# ---------- 3 · LA LOGICA, EN ORDEN ----------
if __name__ == "__main__":
    try:
        a, b = extraer(); cargar(transformar(a, b)); log.info("FIN OK")
    except Exception as error:
        log.error("EL FLUJO FALLO: %s", error); sys.exit(1)
