import logging
import threading
import time


def lock_holder(lock):
    logging.debug('Iniciando')
    while True:
        lock.acquire()
        try:
            logging.debug('Ocupado')
            time.sleep(3)
        finally:
            logging.debug('Disponible')
            lock.release()
        time.sleep(3)


def lector(lock):
    logging.debug('Iniciando')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(3)
        logging.debug('Intentando acceder')
        have_it = lock.acquire(0)
        try:
            num_tries += 1
            if have_it:
                logging.debug('Intento %d: Abierto, puedo entrar',num_tries)
                num_acquires += 1
            else:
                logging.debug('Intento %d: Cerrado, sigue intentando',num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug('Realizado después de %d intentos', num_tries)


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

lock = threading.Lock()

holder = threading.Thread(target=lock_holder,args=(lock,), name='Libro', daemon=True,)
holder.start()

worker = threading.Thread(target=lector, args=(lock,), name='Lector1',)
worker.start()

worker = threading.Thread(target=lector, args=(lock,), name='Lector2',)
worker.start()