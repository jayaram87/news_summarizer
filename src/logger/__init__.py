import logging, os

log_dir = 'src_logging'

os.makedirs(log_dir, exist_ok=True)

log_file_path = 'logs.log'
log_file = os.path.join(log_dir, log_file_path)

logging.basicConfig(
    filename=log_file,
    filemode='a',
    format='[%(asctime)s]|:|%(levelname)s|:|%(lineno)d|:|%(filename)s|:|%(funcName)s()|:|%(message)s',
    level=logging.INFO  
)



