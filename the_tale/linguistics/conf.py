# coding: utf-8
import datetime

from dext.common.utils.app_settings import app_settings

linguistics_settings = app_settings('LINGUISTICS_SETTINGS',
                                    WORDS_ON_PAGE=25,
                                    TEMPLATES_ON_PAGE=25,
                                    MODERATOR_GROUP_NAME='linguistics moderators group',
                                    EDITOR_GROUP_NAME='linguistics editors group',
                                    FORUM_CATEGORY_ID=61,

                                    REMOVED_TEMPLATE_TIMEOUT=30, # days

                                    LINGUISTICS_MANAGER_UPDATE_DELAY=datetime.timedelta(minutes=1))
