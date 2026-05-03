"""Њ®¤г«м гўҐ¤®¬«Ґ­Ё©."""

import logging



logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)





def send_task_assignment_email(user_email: str, task_title: str, project_name: str) -> bool:

    """ЋвЇа ў«пҐв гўҐ¤®¬«Ґ­ЁҐ ® ­ §­ зҐ­ЁЁ § ¤ зЁ."""

    logger.info("[EMAIL] “ўҐ¤®¬«Ґ­ЁҐ ¤«п %%s: § ¤ з  '%%s' ў Їа®ҐЄвҐ '%%s'", user_email, task_title, project_name)

    return True





def send_deadline_reminder(user_email: str, task_title: str, days_left: int) -> bool:

    """ЋвЇа ў«пҐв ­ Ї®¬Ё­ ­ЁҐ ® ¤Ґ¤« ©­Ґ."""

    logger.info("[EMAIL] Ќ Ї®¬Ё­ ­ЁҐ ¤«п %%s: § ¤ з  '%%s' зҐаҐ§ %%s ¤­.", user_email, task_title, days_left)

    return True

