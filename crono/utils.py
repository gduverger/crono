
def seconds(hours=None, minutes=None, seconds=None):
	time = None

	if seconds:
		time = seconds

	if minutes:
		time = (time if time else 0) + (minutes * 60)

	if hours:
		time = (time if time else 0) + (hours * 60 * 60)

	return time
