import os, sys

class CustomException(Exception):
    def __init__(self, error_msg: Exception, error_detail: sys):
        super().__init__(error_msg)
        self.error_msg = CustomException.custom_msg(error_msg, error_detail)

    @staticmethod
    def custom_msg(msg, detail) -> str:
        _, _, try_block = detail.exc_info()
        try_block_nbr = try_block.tb_lineno
        file_name = try_block.tb_frame.f_code.co_filename

        error_msg = f'error occurred in {file_name} at try block nbr {try_block_nbr} with {msg}'

        return error_msg

    def __str__(self):
        return self.error_msg

    def __repr__(self) -> str:
        return CustomException.__name__.str()