"""Flujo de EXPORTACIONES: toma las exportaciones por producto.
Integrantes: Kevin Villamarin
Fuente: datos/exportaciones.csv + datos/catalogo.csv (si es un archivo de EJEMPLO, digalo aqui)
SI FALLA: si la fuente no llega o cambia, el flujo se detiene y sale con código 1"""
import logging, sys
from datetime import date
import pandas as pd

# ---------- 1 · PARAMETROS (todo lo que puede cambiar, junto y arriba) ----------
RUTA_ENTRADA    = "datos/exportaciones.csv"
RUTA_CATALOGO   = "datos/nada.csv"
SALIDA          = f"salida/mi_flujo_{date.today().isoformat()}.csv"
FILAS_ESPERADAS = 7
TOTAL_ESPERADO  = 8679.13   
TOLERANCIA_TOTAL = 0.01 
# agregue aqui otro parametro de comprobacion, por ejemplo un total esperado

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler("flujo.log"), logging.StreamHandler()])
log = logging.getLogger("mi_flujo")

# ---------- 2 · LAS TRES FUNCIONES (cada una con su docstring) ----------
def extraer():
    """Lee exportaciones y catálogo desde CSV y devuelve las dos tablas; falla si falta algún archivo."""
    exportaciones = pd.read_csv(RUTA_ENTRADA)
    catalogo      = pd.read_csv(RUTA_CATALOGO)
    log.info("extraidas %d filas de exportaciones y %d del catalogo",
             len(exportaciones), len(catalogo))
    return exportaciones, catalogo

def transformar(exportaciones, catalogo):
    """Pega el código del catálogo a cada producto; falla si el número de filas o el total no cuadran."""
    if len(exportaciones) != FILAS_ESPERADAS:
        raise ValueError(f"esperaba {FILAS_ESPERADAS} filas y llegaron {len(exportaciones)}")

    # --- transformación: join con el catálogo por el nombre del producto ---
    # Ajusta "producto" al nombre real de la columna en tus dos CSV.
    resultado = exportaciones.merge(catalogo, on="producto", how="left")

    # Si algún producto no encontró código en el catálogo, lo consideramos error.
    if resultado["codigo"].isna().any():
        faltantes = resultado.loc[resultado["codigo"].isna(), "producto"].tolist()
        raise ValueError(f"productos sin código en el catálogo: {faltantes}")

    # --- comprobación del total (detiene el flujo si no cuadra) ---
    total = resultado[COLUMNA_MONTO].sum()
    if abs(total - TOTAL_ESPERADO) > TOLERANCIA_TOTAL:
        raise ValueError(
            f"total esperado {TOTAL_ESPERADO} y obtenido {total:.2f} "
            f"(diferencia {total - TOTAL_ESPERADO:+.2f})"
        )

    log.info("transformadas %d filas, total %.2f OK", len(resultado), total)
    return resultado

def cargar(tabla):
    """Guarda el resultado en salida/ con la fecha del día en el nombre."""
    os.makedirs("salida", exist_ok=True)
    tabla.to_csv(SALIDA, index=False)
    log.info("guardado %s (%d filas)", SALIDA, len(tabla))

# ---------- 3 · LA LOGICA, EN ORDEN ----------
if __name__ == "__main__":
    try:
        exportaciones, catalogo = extraer()
        resultado = transformar(exportaciones, catalogo)
        cargar(resultado)
        log.info("FIN OK")
    except Exception as error:
        log.error("EL FLUJO FALLO: %s", error)
        sys.exit(1)
