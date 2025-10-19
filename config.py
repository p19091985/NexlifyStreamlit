                                                                        

from typing import Dict, Tuple
import os
import configparser                        
from pathlib import Path                

                                                       
_config_path = Path(__file__).parent / "config_settings.ini"
_parser = configparser.ConfigParser()
_parser.read(_config_path)                     

                                                 
def _get_boolean_setting(key, default=False):
    try:
                                                                    
        return _parser.getboolean('Settings', key, fallback=default)
    except (configparser.NoSectionError, configparser.Error):
                                                                            
        return default

                                     
                                                         
DATABASE_ENABLED = _get_boolean_setting('database_enabled', default=True)
INITIALIZE_DATABASE_ON_STARTUP = _get_boolean_setting('initialize_database_on_startup', default=True)
USE_LOGIN = _get_boolean_setting('use_login', default=True)
REDIRECT_CONSOLE_TO_LOG = _get_boolean_setting('redirect_console_to_log', default=False)


                                                  
MAX_LOGIN_ATTEMPTS = 3
                                                                       
                                                                                
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)-15s - %(message)s"

                                                                              