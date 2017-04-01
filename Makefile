.env:
	virtualenv --python=python3 .env

deps: .env
	.env/bin/pip install -r requirements.txt
	.env/bin/pip install -r test-requirements.txt

env: deps
	echo "Run: 'source .env/bin/activate' to activate development environment..."

.PHONY: env
