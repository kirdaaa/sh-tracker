import json
from pathlib import Path

separators = (',', ':')

# Returns IDs of questions that have already been tracked before which are
# stored in 'tracked.json' file
def get_tracked():
	path = Path('tracked.json')

	if not path.is_file():
		return []

	with open(path.name, 'r') as file:
		try:
			tracked = json.load(file)
		except:
			tracked = []

	return tracked

# Saves IDs of tracked questions into 'tracked.json' file
# Used to prevent tracking of questions which already have been tracked
def save_tracked(tracked):
	with open('tracked.json', 'w') as file:
		json.dump(tracked, file, separators=separators)
