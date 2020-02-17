from .mods.mensa_module import get_mensa_menu
from .mods.weather_module import get_weather_for_cities
# Todo build a command processor which are more configuratable and make this for the bots and the modprocesoor!

command_mod_mapping = dict(
	mensa=get_mensa_menu,
	weather=get_weather_for_cities
)

def process_command(input: str) -> str:
	if input.startswith("!"):
		input = input[1:]
	func = command_mod_mapping.get(input.split(" ")[0])
	if func:
		return func(input)