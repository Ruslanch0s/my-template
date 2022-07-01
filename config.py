from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
