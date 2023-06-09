﻿# Python Package Logs

## Introducción

Esta librería contiene funciones para el manejo de logs. La idea es unificar criterios para generar logs en distintos niveles pero con un mismo formato de salida.



## Desarrollo

### Crear archivo `requirements.txt`:

```bash
pipenv requirements > requirements.txt
```

Si en el archivo `requirements.txt` hay una dependencia que viene de Github, deberá estar definida de la siguiente manera:
```txt
<name> @ git+https://github.com/<user>/<repo_name>.git@<id>#egg=<package>
```



### Tests:

```bash
python -m unittest discover -s 'tests' -p 'test_logs.py'
```

### Control de versiones:

```bash
git tag -a <tag> -m "<descripcion>" # Crear tag local
git push origin <tag> 				# Subir tag a repositorio remoto
git tag -d <tag> 					# Eliminar tag en forma local
git push --delete origin <tag>      # Subir tag a repositorio remoto
```



## Instalación

```bash
pipenv install git+https://github.com/lcastiglione/pp-logs.git@<tag>#egg=logs
```



## Ejemplo de uso

```python
from logs.logger import logger,CustomLogger

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