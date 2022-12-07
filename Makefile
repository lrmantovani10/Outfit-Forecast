tests:
	python3 final-src/backend_functions_tests.py -v

setup: requirements.txt
	pip3 install -r requirements.txt
	
clean:
	rm -rf __pycache__
	rm -rf 3a/__pycache__
	rm -rf 3b/__pycache__
	rm -rf 4ab/__pycache__
	rm -rf final-src/__pycache__