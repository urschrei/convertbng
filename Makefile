RUSTDIR = ../latlong_bng
dist/convertbng/convertbng-0.1.12-cp27-none-macosx_10_6_intel.whl: $(RUSTDIR)/target/release/liblonlat_bng.dylib build/lib/convertbng/util.py
	@echo "Rebuilding wheel"
	@export WHEEL_TOOL=/Users/sth/dev/convertbng/venv/bin/wheel
	@echo "Removing build and dist dir"
	@rm -rf build
	@rm -rf dist
	@echo "Packaging source and binary"
	@python setup.py bdist_wheel sdist

$(RUSTDIR)/target/release/liblonlat_bng.dylib: ../latlong_bng/src/lib.rs
	@echo "Rebuilding binary"
	@cd $(RUSTDIR) && cargo test && cargo build --release
	@rm convertbng/liblonlat_bng.dylib
	@cp $(RUSTDIR)/target/release/liblonlat_bng.dylib convertbng/

build/lib/convertbng/util.py: convertbng/util.py
	@# we don't need any rules here, because the main rule rebuilds the wheel


.PHONY: upload
upload:
	@echo "Uploading to PyPI"
	# @twine upload dist/* --sign --identity 39C1ED9A
	@echo "Finished uploading"

.PHONY: clean
clean:
	@echo "Cleaning Rust project"
	@cd $(RUSTDIR) && cargo clean
	@echo "Removing Wheel build and dist dir"
	@rm -rf build
	@rm -rf dist

