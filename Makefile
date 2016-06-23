RUSTDIR = ../lonlat_bng

convertbng/cutil.so: convertbng/cutil.pyx convertbng/cutil.c setup.py convertbng/liblonlat_bng.dylib
	@echo "Rebuilding Cython extension"
	@python setup.py build_ext --inplace

# here's how to build an up-to-date OSX binary
# changing util.{py, pyx} will also trigger a rebuild
convertbng/liblonlat_bng.dylib: $(RUSTDIR)/src/*.rs $(RUSTDIR)/Cargo.toml convertbng/util.py
	@echo "Running Rust tests"
	cargo test --manifest-path=$(RUSTDIR)/Cargo.toml
	@echo  "Rebuilding Rust release binary"
	@cargo build --manifest-path=$(RUSTDIR)/Cargo.toml --release
	@cp $(RUSTDIR)/target/release/liblonlat_bng.dylib convertbng

.PHONY: clean
clean:
	@echo "Cleaning Rust project"
	@cd $(RUSTDIR) && cargo clean
	@echo "Removing Wheel build and dist dir"
	-@rm -rf build
	-@rm -rf dist
	-@rm *.pyc
	-@rm *.rst
	-@rm convertbng/*.pyc
	-@rm convertbng/*.dylib
	-@rm convertbng/*.so
	-@rm convertbng*.c

# rebuild OSX binary if it's out of date, then run Python module tests 
.PHONY: test
test: convertbng/liblonlat_bng.dylib convertbng/cutil.so
	@echo "Running Python module tests"
	@nosetests -v

.PHONY: release
release:
	@rm -rf dist/*
	@echo "Getting latest release from GitHub"
	@python release.py
	@echo "Successfully retrieved release. Uploading to PyPI"
	@twine upload dist/* --sign --identity 39C1ED9A -r pypi
	@echo "Successfully uploaded wheels to PyPI"
