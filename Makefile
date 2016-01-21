RUSTDIR = ../rust_bng
LINUXHOST = ../lonlat_linux_build
# no args: checks for out-of-date binary, rebuilds wheel, and uploads
.PHONY: all
all: build upload

# wheel is always built with up-to-date binary
dist/convertbng/*.whl: convertbng/liblonlat_bng.dylib \
	convertbng/liblonlat_bng.so

# here's how to build an up-to-date OSX binary
# changing util.py will also trigger a rebuild
convertbng/liblonlat_bng.dylib: $(RUSTDIR)/src/lib.rs convertbng/util.py
	@echo "Running rust tests and rebuilding binary"
	@cd $(RUSTDIR) && cargo test && cargo build --release
	-@rm convertbng/liblonlat_bng.dylib
	@cp $(RUSTDIR)/target/release/liblonlat_bng.dylib convertbng/
	@echo "Copied OSX .dylib"

# here's how to build an up-to-date Linux binary
convertbng/liblonlat_bng.so: $(RUSTDIR)/src/lib.rs
	@echo "Rebuilding .so on VM"
	-@rm -rf $(LINUXHOST)/src
	-@rm -rf $(LINUXHOST)/Cargo.toml
	# copy rust source and cargo
	@cp -r $(RUSTDIR)/src $(LINUXHOST)/
	@cp $(RUSTDIR)/Cargo.toml $(LINUXHOST)/
	# build library
	@cd $(LINUXHOST) && vagrant ssh -c \
		'cd /vagrant && cargo build --release \
		&& ar -x /vagrant/target/release/liblonlat_bng.a \
		&& gcc -shared *.o -o /vagrant/target/release/liblonlat_bng.so -lrt \
		'
	# copy python source to VM
	@mkdir -p $(LINUXHOST)/pysrc
	@cp setup.* $(LINUXHOST)/pysrc
	@cp usage.rst $(LINUXHOST)/pysrc
	@cp manifest.in $(LINUXHOST)/pysrc
	@cp -r convertbng/ $(LINUXHOST)/pysrc/convertbng
	-@rm convertbng/liblonlat_bng.so
	# copy linux binary to OSX and VM
	@cp $(LINUXHOST)/target/release/liblonlat_bng.so convertbng/
	@cp $(LINUXHOST)/target/release/liblonlat_bng.so $(LINUXHOST)/pysrc/convertbng
	# clean up
	-@rm $(LINUXHOST)/*.o
	@echo "Copied Linux .so"

# build alone won't upload, but upload will first call build
.PHONY: build
build: dist/convertbng/*.whl
	@nosetests
	@echo "Rebuilding wheel"
	@export WHEEL_TOOL=/Users/sth/dev/convertbng/venv/bin/wheel
	@echo "Removing build and dist dir"
	-@rm -rf build
	-@rm -rf dist
	-@rm -rf *.egg-info
	@echo "Packaging source and binary"
	@python setup.py bdist_wheel sdist

# upload depends on build
.PHONY: upload
upload: build
	# build linux wheel
	-@rm -rf $(LINUXHOST)/pysrc/build
	-@rm -rf $(LINUXHOST)/pysrc/dist
	-@rm -rf $(LINUXHOST)/pysrc/*.egg-info
	@echo "Packaging linux binary"
	@cd $(LINUXHOST) && vagrant ssh -c \
		'cd /vagrant/pysrc && rm -rf build && rm -rf dist \
		&& /vagrant/venv/bin/python setup.py bdist_wheel sdist \
	'
	# PyPi doesn't support binary wheels on Linux ffs
	# cp $(LINUXHOST)/pysrc/dist/*.whl dist/
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
	-@rm convertbng/*.dylib
	-@rm convertbng/*.so

# rebuild OSX binary if it's out of date, then run Python module tests 
.PHONY: test
test: convertbng/liblonlat_bng.dylib
	@echo "Running Python module tests"
	@nosetests -v
