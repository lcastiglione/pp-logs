import json
import unittest
import logging
from logs.logger import logger, CustomLogger
import io

class LoggerTestCase(unittest.TestCase):
    def setUp(self)-> None:
        self.custom_logger=CustomLogger()
        self.custom_logger.set_stream_handler()
        self.custom_logger.remove_json_handler()


    def tearDown(self) -> None:
        self.custom_logger.remove_stream_handler()

    def test_logger_info(self):
        logger.info('Mensaje de info')
        log_contents = self.custom_logger.get_stream_value()
        self.assertLogs(logger=logger, level='INFO')
        self.assertIn('Mensaje de info', log_contents)
        keys=['asctime', 'levelname', 'message']
        output_keys=list(json.loads(log_contents).keys())
        self.assertEqual(keys,output_keys)

    def test_logger_error(self):
        logger.error('Mensaje de error')
        log_contents = self.custom_logger.get_stream_value()
        self.assertLogs(logger=logger, level='ERROR')
        self.assertIn('Mensaje de error', log_contents)
        keys=['asctime', 'levelname', 'message', 'filename', 'funcName', 'levelno', 'lineno', 'module', 'pathname', 'process', 'processName', 'thread']
        output_keys=list(json.loads(log_contents).keys())
        self.assertEqual(keys,output_keys)


    def test_logger_set_level(self):
        # Set log level to DEBUG
        CustomLogger().set_level(logging.ERROR)
        logger.debug('Mensaje de depuración')
        log_contents = self.custom_logger.get_stream_value()
        self.assertNotIn('Mensaje de depuración', log_contents)
        logger.error('Mensaje de error')
        log_contents = self.custom_logger.get_stream_value()
        self.assertIn('Mensaje de error', log_contents)


