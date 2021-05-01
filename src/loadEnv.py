from os import environ, path

from dotenv import load_dotenv

load_dotenv()

basedir = path.abspath(path.dirname('./'))
env = environ.get('ENV', 'production')
env_loaded = load_dotenv(path.join(basedir, f'.env.{env}'), verbose=True)