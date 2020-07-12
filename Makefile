
go:
	pylint query.py
	./query.py

clean:
	cd data && make clean

veryclean: clean
	cd data && make veryclean


