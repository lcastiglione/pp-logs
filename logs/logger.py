from pythonjsonlogger import jsonlogger
from typing import Dict, Any
import logging
import io


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Formateador personalizado para logs en formato JSON."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CustomJsonFormatter, self).__init__(*args, **kwargs)
        # Necesario para que se cargue la hora local de creación del log
        self._required_fields.append('asctime')

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        """Agrega campos personalizados al registro de log.

        Args:
            log_record (Dict[str, Any]): Registro de log actual.
            record (logging.LogRecord): Registro de log.
            message_dict (Dict[str, Any]): Diccionario con información del mensaje.
        """

        self._fmt = '%(asctime)s %(levelname)s %(message)s'
        if record.levelno >= logging.ERROR:
            self._fmt += ' %(filename)s %(funcName)s %(levelno)s %(lineno)d %(module)s %(pathname)s %(process)d %(processName)s %(thread)d %(exc_info)s'
        self._required_fields = self.parse()
        super().add_fields(log_record, record, message_dict)


class CustomLogger:
    """Clase Singleton para la configuración del logger."""

    _instance: 'CustomLogger' = None

    def __new__(cls, *args: Any, **kwargs: Any) -> 'CustomLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = None
            cls._instance.configure_logger()
        return cls._instance

    def configure_logger(self, level: int = logging.INFO) -> None:
        """Configura el logger con el nivel de log especificado.

        Args:
            level (int): Nivel de log a establecer.
        """
        self.handlers = {}
        self.logger = logging.getLogger()
        self.set_json_handler()
        self.logger.setLevel(level)

    def set_json_handler(self) -> None:
        """Agrega un manejador de logs en formato JSON al logger."""
        logHandler = logging.StreamHandler()
        formatter = CustomJsonFormatter()
        logHandler.setFormatter(formatter)
        self.logger.addHandler(logHandler)
        self.handlers['json'] = {'logHandler': logHandler}

    def remove_json_handler(self) -> None:
        """Remueve el manejador de logs en formato JSON del logger."""
        self.logger.removeHandler(self.handlers['json']['logHandler'])
        self.handlers['json']['logHandler'].close()

    def set_stream_handler(self) -> None:
        """Agrega un manejador de logs en formato de flujo al logger."""
        log_stream = io.StringIO()
        logHandler = logging.StreamHandler(log_stream)
        formatter = CustomJsonFormatter()
        logHandler.setFormatter(formatter)
        self.logger.addHandler(logHandler)
        self.handlers['io'] = {
            'logHandler': logHandler, 'log_stream': log_stream}

    def remove_stream_handler(self) -> None:
        """Remueve el manejador de logs en formato de flujo del logger."""
        self.logger.removeHandler(self.handlers['io']['logHandler'])
        self.handlers['io']['logHandler'].close()
        self.handlers['io']['log_stream'].close()

    def get_stream_value(self):
        return CustomLogger().handlers['io']['log_stream'].getvalue()

    def set_level(self, level: int) -> None:
        """Establece el nivel de log del logger.

        Args:
            level (int): Nivel de log a establecer.
        """
        if self.logger is None:
            self.configure_logger(level)
        else:
            self.logger.setLevel(level)


logger: logging.Logger = CustomLogger().logger
