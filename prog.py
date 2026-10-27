import schedule, time, subprocess, sys, logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

INTERVALO_SEG = 20      # en clase: cada 20 segundos. En real seria: schedule.every().day.at("12:00")
DURACION_SEG  = 70      # el programa se detiene solo, para no dejar la celda o la terminal tomada

def correr():
    r = subprocess.run([sys.executable, "flujo_exportaciones.py"], capture_output=True, text=True)
    logging.info("el flujo termino con codigo %d", r.returncode)

schedule.every(INTERVALO_SEG).seconds.do(correr)
fin = time.time() + DURACION_SEG
while time.time() < fin:
    schedule.run_pending()
    time.sleep(1)
logging.info("programador detenido")
