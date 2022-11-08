tests:
	python3 3b/backend_functions_tests.py -v

setup: requirements.txt
	pip3 install -r requirements.txt
	
clean:
	rm -rf __pycache__