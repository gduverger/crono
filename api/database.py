import os

from airtable import airtable

db = airtable.Airtable(os.getenv('AIRTABLE_BASE_ID'), os.getenv('AIRTABLE_API_KEY'))

def has_user(token=None):
	records = db.get('Users')['records']
	print([r['id'] for r in records])
	return True
