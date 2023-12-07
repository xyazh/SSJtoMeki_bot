from .MailHellper import MailHelper
from ..xyazhServer.DataManager import DataManager

class C:
    H = "http"
    IP_CHECK_MAIL_TIMER = {}
    user_data_manager = DataManager("\\user_data\\")
    temp_mail_data_manager = DataManager("\\temp_mail_data\\")
    msg_data_manager = DataManager("\\msg_data\\")
    mail_helper = MailHelper()