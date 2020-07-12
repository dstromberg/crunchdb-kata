
go:
	pylint query.py
	cd data && make
	./query.py --most-frequently-owned-car-brand
	cd data && make
	./query.py --favorite-car-brand
	cd data && make
	./query.py --most-frequently-listened-music-artist
	cd data && make
	./query.py --favourite-music-artist

clean:
	cd data && make clean

veryclean: clean
	cd data && make veryclean


