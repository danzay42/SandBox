
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="MY_APP",
    environments=True,
    env_switcher="MY_APP_ENV",
    settings_files=['settings.yaml', '.secrets.yaml'],
)
