"""
Acquire runtime configuration from environment variables (etc).
"""

import os
import yaml


def logfile_path(jsonfmt=False, debug=False):
    """
    Returns the a logfileconf path following this rules:
      - conf/logging_debug_json.conf # jsonfmt=true,  debug=true
      - conf/logging_json.conf       # jsonfmt=true,  debug=false
      - conf/logging_debug.conf      # jsonfmt=false, debug=true
      - conf/logging.conf            # jsonfmt=false, debug=false
    Can be parametrized via envvars: JSONLOG=true, DEBUGLOG=true
  """
    _json = ""
    _debug = ""

    if jsonfmt or os.getenv('JSONLOG', 'false').lower() == 'true':
        _json = "_json"

    if debug or os.getenv('DEBUGLOG', 'false').lower() == 'true':
        _debug = "_debug"

    return os.path.join(PROMSNAPS_CONF_DIR, "logging%s%s.conf" % (_debug, _json))


def getenv(name, default=None, convert=str):
    """
    Fetch variables from environment and convert to given type.

    Python's `os.getenv` returns string and requires string default.
    This allows for varying types to be interpolated from the environment.
    """

    # because os.getenv requires string default.
    internal_default = "(none)"
    val = os.getenv(name, internal_default)

    if val == internal_default:
        return default

    if callable(convert):
        return convert(val)

    return val


def envbool(value: str):
    return value and (value.lower() in ('1', 'true'))


APP_ENVIRON = getenv("APP_ENV", "development")

PROMSNAPS_API = getenv("PROMSNAPS_API", "https://promsnaps.example.com")
PROMSNAPS_SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMSNAPS_ROOT_DIR = os.path.abspath(os.path.join(PROMSNAPS_SOURCE_DIR, "../"))
PROMSNAPS_CONF_DIR = os.getenv("PROMSNAPS_CONF_DIR", os.path.join(
    PROMSNAPS_ROOT_DIR, "conf/"))
PROMSNAPS_CONF_FILE = os.getenv("PROMSNAPS_CONF_FILE", None)


class PrometheusSnapsConfig(object):
    """
    """

    def __init__(self, defaults=None, confpath=None):
        self.settings = {
            'promsnaps': {
                'debug': False,
                'env': APP_ENVIRON,
                'url': PROMSNAPS_API,
            },
        }
        if defaults:
            self.load_conf(defaults)

        if confpath:
            self.load_conffile(confpath)

    @property
    def gitlab(self):
        return self.settings['gitlab']

    @property
    def github(self):
        return self.settings['github']

    @property
    def promsnaps(self):
        return self.settings['promsnaps']

    def reload(self, confpath, inplace=False):
        if inplace:
            instance = self
            instance.load_conffile(confpath)
        else:
            instance = PrometheusSnapsConfig(defaults=self.settings, confpath=confpath)

        return instance

    def load_conf(self, conf):
        for key, v in conf.items():
            self.settings[key].update(v)

    def load_conffile(self, confpath):
        with open(confpath, 'r') as conffile:
            self.load_conf(yaml.load(conffile.read()))


GCONFIG = PrometheusSnapsConfig(confpath=PROMSNAPS_CONF_FILE)
