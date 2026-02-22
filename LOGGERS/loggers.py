import logging

basic_logger_config = "%(levelname)s | %(name)s | %(message)s"

def create_logger(logger_name):
    logging.basicConfig(
        level = logging.INFO,  
        format = basic_logger_config,
    )

    return logging.getLogger(logger_name)