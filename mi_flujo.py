"""Flujo de ___ : (una linea que diga que hace).
Integrantes: ___
Fuente: ___ (si es un archivo de EJEMPLO, digalo aqui)
SI FALLA: ___ (que pasa si la fuente no llega o cambia, y A QUIEN habria que avisar)"""
import logging, sys
from datetime import date
import pandas as pd

# ---------- 1 · PARAMETROS (todo lo que puede cambiar, junto y arriba) ----------
RUTA_ENTRADA    = "___"
SALIDA          = f"salida/mi_flujo_{date.today().isoformat()}.csv"
FILAS_ESPERADAS = ___
# agregue aqui otro parametro de comprobacion, por ejemplo un total esperado

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler("flujo.log"), logging.StreamHandler()])
log = logging.getLogger("mi_flujo")

# ---------- 2 · LAS TRES FUNCIONES (cada una con su docstring) ----------
def extraer():
    """___ (que hace esta funcion)"""
    tabla = pd.read_csv(RUTA_ENTRADA)
    log.info("extraidas %d filas", len(tabla))
    return tabla

def transformar(tabla):
    """___ (que hace esta funcion)"""
    if len(tabla) != FILAS_ESPERADAS:
        raise ValueError(f"esperaba {FILAS_ESPERADAS} filas y llegaron {len(tabla)}")
    # AQUI: su transformacion y SU comprobacion que detiene (otro raise).
    return tabla

def cargar(tabla):
    """___ (que hace esta funcion)"""
    import os; os.makedirs("salida", exist_ok=True)
    tabla.to_csv(SALIDA, index=False)
    log.info("guardado %s (%d filas)", SALIDA, len(tabla))

# ---------- 3 · LA LOGICA, EN ORDEN ----------
if __name__ == "__main__":
    try:
        cargar(transformar(extraer())); log.info("FIN OK")
    except Exception as error:
        log.error("EL FLUJO FALLO: %s", error); sys.exit(1)
