RUSTDIR = ../lonlat_bng
LINUXHOST = ../lonlat_linux_build

# here's how to build an up-to-date OSX binary
# changing util.py will also trigger a rebuild
convertbng/util/liblonlat_bng.dylib: $(RUSTDIR)/src/lib.rs convertbng/util.py
	@echo "Running rust tests and rebuilding binary"
	@cd $(RUSTDIR) && cargo test && cargo build --release && strip -ur target/release/liblonlat_bng.dylib
	-@rm convertbng/liblonlat_bng.dylib
	@cp $(RUSTDIR)/target/release/liblonlat_bng.dylib convertbng/
	@echo "Copied OSX .dylib"

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
test: convertbng/util/liblonlat_bng.dylib
	-@rm convertbng/cutil.c
	-@rm convertbng/cutil.so
	-@python setup.py build_ext --inplace
	@echo "Running Python module tests"
	@nosetests -v
