# -*- coding: utf-8 -*-
import os
from cms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Meilisearch connection parameters
MEILISEARCH_ENABLED = True
MEILISEARCH_URL = "http://meilisearch:7700"
MEILISEARCH_PUBLIC_URL = "http://meilisearch.www.myopenedx.com"
MEILISEARCH_INDEX_PREFIX = "tutor_"
MEILISEARCH_API_KEY = "8409083f34402c541580f1dec6174b90ec7bd22108120c53a69ae9ae091897f7"
MEILISEARCH_MASTER_KEY = "2BpyzGCFcGpz7GH1GuUAbwSO"
SEARCH_ENGINE = "search.meilisearch.MeilisearchEngine"

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "My Open edX - http://www.myopenedx.com"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

# REMOVE-AFTER-V20: check if we can remove these lines after upgrade.
try:
    from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
    # RemovedInDjango5xWarning: 'xxx' is deprecated. Use 'yyy' in 'zzz' instead.
    warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
    warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)
    # DeprecationWarning: 'imghdr' is deprecated and slated for removal in Python 3.13
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="pgpy.constants")
except ImportError:
    pass # If the warnings don't exist we don't need to filter them.
    
# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://www.myopenedx.com/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "i6TCkGN0AqtaZQPAk2rOo2V9"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "BDZfDhswRIquOjTIRzUEyECP3kq7HslbObJGAKrNzo-oiSE7acpPnUB5GhC2tw8CWSFYTrjkgQPEOIUKVfysli4t_zMg61c3mFNrCdvwl-1dp6wwthdRE83-GNgwehzT3e2PbI9xqQxz97YPf-WIzfi5DNZhIoloMcih76q8EtXxMtfYaEWDG6A8bnaGkouXwi9Xv0ozsPTRvrnmNMg3_LDIGAzAVznV7l9-2zzkAGfdrtDAnu57ZI7Bg79daKVZv379uk5h7uNgbLikVWqTqo_-BbsF1K378EDkmklR0hA0iSkTCoNic6GIg5PijJa36Jj2hJeB2Hz6R9Q5Xpe9oQ",
        "n": "uMiy-TAK65mpyl5TnjV1w-oWbA3zPL2EdtUcQ07nN20q-Rsqq6XES2jtlhKjxgkmv9ya6e4L-pAlvxoxLsflEqMoVS74innR_9S12iCia0JpuxcG5vzF7rSWly590vyRx1sMW6aXj0UOw7BbfqKP2eD9LtpMPMBh3-1yK_soXZFNtbeWmf2vkCa98CNfRIfP7BYIC9vkZWihIW3qA8XOuz5Wgs_hWhq-K9EYbwMJEy2kH10KM2T2jVNvVTFe60piyDx-JN7gUJRfo7qZGaxQ6SAHISl8eK5fTQX1dcgKNJEf14iZM9lRpOyiokgAl4f8fFbAAsaCMTV5Nnz7VsWZuw",
        "p": "yMTq0alDHF6wWP9otf-zdoajMWZ4tFRvC79tlxr9fJxBYYSMEgE-7GwfYpnL3sY9upIZZqNMTEna2sx8TIcwXlWQ2vo0uSPj4D5Ozp01i1HVZK2dEB8z0eBykWd2zjxk11nrcWBC4s6cHMiw97jninFsYIbEoMjedmFwM8mU33k",
        "q": "654HgAlq1MwibARxJSTt__0T68kJkujKg0whEE7V5au1MomZwwN-v4y6wKx6H3Re7usXLxj9MXQcCacOqYWOeCMJVB9WJkV7fwlkwZDexLXZyOG4XVJQSz3TVG6haKBvsXeDE1W-BXP2Bix0vhQ2zrCijoLbbDQbl213f3GVcdM",
        "dq": "ndqDBdnJVAXrbdjQAOWr-hwQs6A9pMoHm01uvWFD1ppiTBh6BngZ-7UKDTnAm8A4NfMU1j30q6QxgJoGrbZHy98VSeGwsvVMFsExWql3RezbmsT24rbaCn7CTcfMpa8PBaOfEl4Yb8jP5DT2hb4_NdyLG9U5slV6wsnZDG4JhHc",
        "dp": "qgcKjtD4Avi2BEkZlricdc6EOnv70UyIVryhxQyYjIWQYVPtg_oGHhdbZRe2rk3ZTT4ZwPCe1yTc8dunkPAUqG9yo-Ct8fVRMUHTX-uHwxtky0S09UhXjHC21il3ViWTiUWfvX62Znpvf3j_VmwDux1fmUfJEhnLPRo7-b_IEpE",
        "qi": "Py5aYki9WHNc80tpjatqJX_BIjZ_WInmFGudBfkyz7yVllmWy8AkZ8M4RWi5vNRzSrf7SFu2-1K4Ol1G2x9qA4_G3j8j_vmfmVWNsQ37JrxktKUhFm4HOaseXbNbJZYLceE7kmqSwjaESuOHgZOQKcbFeSgdJo4U3cc2P5igM4E",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "uMiy-TAK65mpyl5TnjV1w-oWbA3zPL2EdtUcQ07nN20q-Rsqq6XES2jtlhKjxgkmv9ya6e4L-pAlvxoxLsflEqMoVS74innR_9S12iCia0JpuxcG5vzF7rSWly590vyRx1sMW6aXj0UOw7BbfqKP2eD9LtpMPMBh3-1yK_soXZFNtbeWmf2vkCa98CNfRIfP7BYIC9vkZWihIW3qA8XOuz5Wgs_hWhq-K9EYbwMJEy2kH10KM2T2jVNvVTFe60piyDx-JN7gUJRfo7qZGaxQ6SAHISl8eK5fTQX1dcgKNJEf14iZM9lRpOyiokgAl4f8fFbAAsaCMTV5Nnz7VsWZuw",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://www.myopenedx.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "i6TCkGN0AqtaZQPAk2rOo2V9"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
# Note: CORS_ALLOW_HEADERS is intentionally not defined here, because it should
# be consistent across deployments, and is therefore set in edx-platform.

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

OPENEDX_LEARNING = {
    'MEDIA': {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": "/openedx/media-private/openedx-learning",
        }
    }
}

# edx-event-bus-redis settings
EVENT_BUS_PRODUCER = 'edx_event_bus_redis.create_producer'
EVENT_BUS_REDIS_CONNECTION_URL = 'redis://@redis:6379/'
EVENT_BUS_TOPIC_PREFIX = 'dev'
EVENT_BUS_CONSUMER = 'edx_event_bus_redis.RedisEventConsumer'


######## End of settings common to LMS and CMS

######## Common CMS settings
STUDIO_NAME = "My Open edX - Studio"

CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_cms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_cms",
}

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "QnuI5wdLNqDuJjJZisCeTQ2g"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Enable "reindex" button
FEATURES["ENABLE_COURSEWARE_INDEX"] = True

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)



######## End of common CMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
]
CORS_ORIGIN_WHITELIST.append("http://studio.www.myopenedx.com")

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://www.myopenedx.com"

# MFE-specific settings

COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.www.myopenedx.com/authoring"


LOGIN_REDIRECT_WHITELIST.append("apps.www.myopenedx.com")
CORS_ORIGIN_WHITELIST.append("http://apps.www.myopenedx.com")
CSRF_TRUSTED_ORIGINS.append("http://apps.www.myopenedx.com")