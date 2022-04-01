default: env

env:
	python3 -m venv env
	env/bin/pip install --upgrade pip setuptools wheel
	env/bin/pip install -r requirements.txt

.PHONY: run clean
	
run:
	env/bin/python game.py

clean:
	rm -rf env

