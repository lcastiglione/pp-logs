# Python Package Logs

## Introducción

Esta librería contiene funciones para el manejo de logs. La idea es unificar criterios para generar logs en distintos niveles pero con un mismo formato de salida.



## Desarrollo

Crear archivo `requirements.txt`:

```bash
pipenv requirements > requirements.txt
```

Tests:

```bash
python -m unittest discover -s 'tests' -p 'test_logs.py'
```



## Instalación

```bash
pipenv install git+https://github.com/lcastiglione/pp-logs#egg=logs
```



## Ejemplo de uso

```python
from logs.logs import logger,CustomLogger

# Imprimir log en pantalla
print(logger.info('test'))
print(logger.debug('test'))
print(logger.error('test'))

# La instancia de CustomLogger es única
custom_logger = CustomLogger()

#Imprimir solo logs de nivel `ERROR` o superior
custom_logger.set_level(logging.ERROR)

# Cargar el handler mostrar por consola los mensajes en formato JSON
# (Se hace por default)
custom_logger.set_json_handler()

# Remover el handler JSON
custom_logger.remove_json_handler()

# Cargar el handler para guardar los logs en una variable y que no
# salgan por consola
custom_logger.set_stream_handler()
log_contents = custom_logger.get_stream_value()
print(log_contents)

# Remover el handler que guarda los logs en una variable
custom_logger.remove_stream_handler()
```