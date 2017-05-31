.env:
	virtualenv --python=python3 .env

.env/deps: .env
	.env/bin/pip install -r requirements.txt
	.env/bin/pip install -r test-requirements.txt
	touch .env/deps

sqlite.db: .env/deps
	.env/bin/python manage.py migrate

.env/populated: sqlite.db
	.env/bin/python manage.py populate
	.env/bin/python manage.py add-consumption
	.env/bin/python manage.py add-production
	touch .env/populated

startserver: .env/populated
	.env/bin/python manage.py runserver

