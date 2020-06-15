import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .base import *

env_name = os.getenv('ENV_NAME')

if env_name == 'prod':
    from .prod import *
else:
    from .dev import *