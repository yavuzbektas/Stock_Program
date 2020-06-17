import logging

class MyLogger():
    LOG_FILENAME = '/media/logs/myapp.log'
    # create logger
    my_logger = logging.getLogger("Stock-V0")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=LOG_FILENAME,
                        filemode='w')
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
                  LOG_FILENAME, maxBytes=20, backupCount=5)
    my_logger.addHandler(handler)

