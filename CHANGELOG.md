# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-10-11

### Removed

- **Breaking:** the ctypes interface in `convertbng.util`. Use `convertbng.cutil` instead, which accepts the same inputs, but returns a tuple of two float64 NumPy arrays rather than two lists. Two functions have different names in `convertbng.cutil`: `convert_osgb36_to_lonlat` is `convert_osgb36_to_ll`, and `convert_etrs89_to_lonlat` is `convert_etrs89_to_ll`.
- **Breaking:** support for Python 3.10.

### Changed

- **Breaking:** inputs of different lengths raise `ValueError`. Previously, some of the returned values were silently left unconverted, and `convertbng.util` could read past the end of the shorter input.
- **Breaking:** multi-dimensional arrays raise `ValueError`. Previously, `convertbng.util` silently converted only part of a two-dimensional array.
- **Breaking:** non-numeric input raises `TypeError`. Previously, `convertbng.cutil` raised `ValueError` or converted numeric strings such as `"1.7"`, and `convertbng.util` raised `ctypes.ArgumentError`.
- **Breaking:** the conversion functions' arguments are positional-only.
- The extension is now built from the Rust [lonlat_bng](https://crates.io/crates/lonlat_bng) crate using [PyO3](https://pyo3.rs) and [maturin](https://www.maturin.rs), replacing the Cython wrapper around the prebuilt lonlat_bng library. The wheel no longer bundles a separate shared library. Results are unchanged.
- The GIL is released while converting.
- Conversion is faster, especially for small inputs.

### Added

- The `convertbng.cutil` functions accept single numbers (including zero-dimensional NumPy arrays), generators and other iterables, and empty inputs.
- Type stubs for `convertbng.cutil`, with a `py.typed` marker ([PEP 561](https://peps.python.org/pep-0561/)).
- The source distribution can now be built and installed on platforms without a prebuilt wheel, given a Rust toolchain.
- The extension module declares support for free-threaded CPython builds.

## [1.0.0] and earlier

See the [commit history](https://github.com/urschrei/convertbng/commits/v1.0.0).

[2.0.0]: https://github.com/urschrei/convertbng/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/urschrei/convertbng/releases/tag/v1.0.0
