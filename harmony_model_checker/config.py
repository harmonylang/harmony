
import json
import os
import pathlib
from typing import NamedTuple


class Setting(NamedTuple):
    disable_web: bool

def _make_new_settings():
    return Setting(
        disable_web=False,
    )
_default_settings = _make_new_settings()


class SettingsManager:
    def __init__(self) -> None:
        self.user_dir = self._setup_harmony_dir()
        self.settings_file = self._setup_settings_file()
        
        self.values = self._load_settings_file()
        self._update_from_env()

    def update_settings_file(self, attr, value):
        value_type = type(_default_settings.__getattribute__(attr))        

        with self.settings_file.open('r') as f:
            d = json.load(f)
        
        if value_type == bool:
            v = str(value).lower() == 'true'
        else:
            raise ValueError(value)

        d[attr] = v
        with self.settings_file.open('w') as f:
            json.dump(d, f)

    def get_settings_value(self, attr):
        return self.values.__getattribute__(attr)

    def _setup_harmony_dir(self):
        """Create a application-specific directory following the XDG specification."""
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME', str(pathlib.Path.home() / ".config"))
        user_dir = pathlib.Path(xdg_config_home, 'harmony-model-checker').expanduser()
        if not user_dir.is_dir():
            user_dir.mkdir(parents=True)
        return user_dir

    def _setup_settings_file(self):
        settings_path = self.user_dir.joinpath('settings.json')
        if not settings_path.is_file():
            s = _make_new_settings()
            with settings_path.open('w') as f:
                json.dump(s._asdict(), f)
        return settings_path

    def _load_settings_file(self):
        with self.settings_file.open('r') as f:
            try:
                d: dict = json.load(f)
                return Setting({'disable_update_check': d.get('disable_update_check')})
            except TypeError:
                return _make_new_settings()

    def _update_from_env(self):
        val = os.environ.get('HARMONY_DISABLE_WEB', None)
        if val is not None:
            self.values.disable_web = val.lower() == 'true'


settings = SettingsManager()
