go:
	python3 -m pylint --rcfile ../pylintrc *.py
	# python3 -m pytest
	python3 generate_data.py 55

deps:
	python3 -m pip install -r requirements.txt

clean:
	rm -rf __pycache__

veryclean: clean
	find ../json-data/ -type f -print0 | xargs -0 --no-run-if-empty rm -fv
