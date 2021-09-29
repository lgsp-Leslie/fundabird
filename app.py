from flask_migrate import Migrate
from apps.models.mall_models import *
from apps.models.config_models import *
from apps.models.manage_models import *
from apps import create_app
from config.exts import db

app = create_app()

# 命令工具
migrate = Migrate(app=app, db=db)
