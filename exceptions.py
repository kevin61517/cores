"""
錯誤類
"""
INVALID_REQUEST = 'invalid_request'
INVALID_OPTION = 'invalid_options'


class BaseError(Exception):
    """錯誤基類"""

    def __init__(self, message="ServerError"):
        super().__init__(message)

    def to_json(self):
        return {}


class DBError(BaseError):
    """DB Error"""
    status_code = 500  # http狀態碼
    content_status = 500  # 與對接端約定以及工程人員判讀的伺服器錯誤碼
    type_ = 'invalid_option_error'  # 錯誤類型
    message = '資料錯誤'  # 錯誤訊息

    def __init__(self, msg=None, status_code=None, payload=None, content_status=None):
        """
        :param msg: 錯誤訊息
        :param status_code: http狀態
        :param payload: 錯誤內容
        :param content_status: 響應內容狀態
        """
        if msg is not None:
            self.message = msg
        if status_code is not None:
            self.status_code = status_code
        if content_status is not None:
            self.content_status = content_status
        if payload is None:
            payload = {
                'failure_code': self.content_status,
                'failure_msg': self.message,
            }
        self.payload = payload
        super().__init__(self.message)

    def to_json(self):
        return dict(
            type=self.type_,
            msg=self.message,
            status=self.content_status,
            payload=self.payload)


#####################
#      DB ERROR     #
#####################
class DBOptionError(DBError):
    """操作錯誤"""
    content_status = 50000
    message = '資料庫操作錯誤'
    type_ = INVALID_OPTION


class DBOrmError(DBError):
    """ORM錯誤"""
    content_status = 50001
    message = '伺服器ORM錯誤'
    type_ = INVALID_OPTION
