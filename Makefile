RUSTDIR = ../rust_bng
# no args: checks for out-of-date binary, rebuilds wheel, and uploads
.PHONY: all
all: build upload

# wheel is always built with up-to-date binary
dist/convertbng/convertbng-0.1.12-cp27-none-macosx_10_6_intel.whl: convertbng/liblonlat_bng.dylib \
	convertbng/liblonlat_bng.so

# here's how to build an up-to-date OSX binary
convertbng/liblonlat_bng.dylib: $(RUSTDIR)/src/lib.rs
	@echo "Running rust tests and rebuilding binary"
	@cd $(RUSTDIR) && cargo test && cargo build --release
	-@rm convertbng/liblonlat_bng.dylib
	@cp $(RUSTDIR)/target/release/liblonlat_bng.dylib convertbng/
	@echo "Copied OSX .dylib"

# here's how to build an up-to-date Linux binary
convertbng/liblonlat_bng.so: $(RUSTDIR)/src/lib.rs
	@echo "Rebuilding .so on VM"
	-@rm -rf ../lonlat_linux_build/src
	-@rm -rf ../lonlat_linux_build/Cargo.toml
	# copy rust source and cargo
	@cp -r $(RUSTDIR)/src ../lonlat_linux_build/
	@cp $(RUSTDIR)/Cargo.toml ../lonlat_linux_build/
	# build library
	@cd ../lonlat_linux_build && vagrant ssh -c \
		'cd /vagrant && cargo build --release \
		&& ar -x /vagrant/target/release/liblonlat_bng.a \
		&& gcc -shared *.o -o /vagrant/target/release/liblonlat_bng.so -lrt \
		'
	# copy python source to VM
	@cp setup.* ../lonlat_linux_build/pysrc
	@cp usage.rst ../lonlat_linux_build/pysrc
	@cp manifest.in ../lonlat_linux_build/pysrc
	@cp -r convertbng/ ../lonlat_linux_build/pysrc/convertbng
	-@rm convertbng/liblonlat_bng.so
	# copy linux binary to OSX and VM
	@cp ../lonlat_linux_build/target/release/liblonlat_bng.so convertbng/
	@cp ../lonlat_linux_build/target/release/liblonlat_bng.so ../lonlat_linux_build/pysrc/convertbng
	# clean up
	-@rm ../lonlat_linux_build/*.o
	@echo "Copied Linux .so"

# build alone won't upload, but upload will first call build
.PHONY: build
build: dist/convertbng/convertbng-0.1.12-cp27-none-macosx_10_6_intel.whl
	@nosetests

# upload depends on build
.PHONY: upload
upload: build
	@echo "Rebuilding wheel"
	@export WHEEL_TOOL=/Users/sth/dev/convertbng/venv/bin/wheel
	@echo "Removing build and dist dir"
	-@rm -rf build
	-@rm -rf dist
	-@rm -rf *.egg-info
	-@rm -rf ../lonlat_linux_build/pysrc/build
	-@rm -rf ../lonlat_linux_build/pysrc/dist
	-@rm -rf ../lonlat_linux_build/pysrc/*.egg-info
	@echo "Packaging source and binary"
	@python setup.py bdist_wheel sdist
	# build linux wheel
	@echo "Packaging linux binary"
	@cd ../lonlat_linux_build && vagrant ssh -c \
		'cd /vagrant/pysrc && rm -rf build && rm -rf dist \
		&& /vagrant/venv/bin/python setup.py bdist_wheel sdist \
	'
	# PyPi doesn't support binary wheels on Linux ffs
	# cp ../lonlat_linux_build/pysrc/dist/*.whl dist/
	@echo "Uploading to PyPI"
	@twine upload dist/* --sign --identity 39C1ED9A
	@echo "Finished uploading"

.PHONY: clean
clean:
	@echo "Cleaning Rust project"
	@cd $(RUSTDIR) && cargo clean
	@echo "Removing Wheel build and dist dir"
	-@rm -rf build
	-@rm -rf dist
	-@rm *.pyc
	-@rm convertbng/*.pyc

# rebuild OSX binary if it's out of date, then run Python module tests 
.PHONY: test
test: convertbng/liblonlat_bng.dylib
	@echo "Running Python module tests"
	@nosetests -v
