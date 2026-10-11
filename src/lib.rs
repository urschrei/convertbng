//! Python bindings for the [`lonlat_bng`](https://crates.io/crates/lonlat_bng) crate.
//!
//! Every function takes two inputs of equal length (e.g. longitudes and latitudes), converts each
//! pair in parallel without holding the GIL, and returns two float64 NumPy arrays. Pairs that
//! can't be converted (e.g. because they're outside the OSTN15 grid) become `(nan, nan)`.

use numpy::{PyArray1, PyUntypedArray};
use pyo3::buffer::PyBuffer;
use pyo3::exceptions::{PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyByteArray, PyBytes, PyString};

type Converted<'py> = (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>);
type Converter = for<'a> fn(&'a mut [f64], &'a mut [f64]) -> (&'a mut [f64], &'a mut [f64]);

fn not_a_number(e: PyErr, py: Python<'_>) -> PyErr {
    let err = PyTypeError::new_err("expected a number, or an iterable of numbers");
    err.set_cause(py, Some(e));
    err
}

/// Copy `values` into a `Vec`.
///
/// Any object exposing a one-dimensional float64 buffer (e.g. a NumPy array, contiguous or not)
/// is read directly. NumPy arrays of other dtypes are converted to float64 first. Otherwise,
/// `values` can be any iterable of numbers (including a generator), or a single number.
fn extract_values(values: &Bound<'_, PyAny>) -> PyResult<Vec<f64>> {
    let py = values.py();
    if values.is_instance_of::<PyString>()
        || values.is_instance_of::<PyBytes>()
        || values.is_instance_of::<PyByteArray>()
    {
        return Err(PyTypeError::new_err(format!(
            "expected a number, or an iterable of numbers, not {}",
            values.get_type().name()?
        )));
    }
    let buf = match PyBuffer::<f64>::get(values) {
        Ok(buf) => Some(buf),
        // NumPy won't export a buffer for a zero-dimensional array, which is read as a number below
        Err(_) if values.is_instance_of::<PyUntypedArray>() => {
            PyBuffer::get(&values.call_method1("astype", ("float64",))?).ok()
        }
        Err(_) => None,
    };
    if let Some(buf) = buf {
        match buf.dimensions() {
            0 => return Ok(vec![values.extract::<f64>()?]),
            1 => {}
            _ => {
                return Err(PyValueError::new_err(format!(
                    "expected a one-dimensional array, got shape {:?}",
                    buf.shape()
                )));
            }
        }
        return match buf.as_slice(py) {
            Some(cells) => Ok(cells.iter().map(|c| c.get()).collect()),
            None => buf.to_vec(py),
        };
    }
    match values.try_iter() {
        Ok(iter) => iter
            .map(|item| item?.extract::<f64>().map_err(|e| not_a_number(e, py)))
            .collect(),
        Err(_) => Ok(vec![
            values.extract::<f64>().map_err(|e| not_a_number(e, py))?,
        ]),
    }
}

fn convert<'py>(
    x: &Bound<'py, PyAny>,
    y: &Bound<'py, PyAny>,
    converter: Converter,
) -> PyResult<Converted<'py>> {
    let py = x.py();
    let mut xs = extract_values(x)?;
    let mut ys = extract_values(y)?;
    if xs.len() != ys.len() {
        return Err(PyValueError::new_err(format!(
            "inputs must have the same length, got {} and {}",
            xs.len(),
            ys.len()
        )));
    }
    py.detach(|| {
        converter(&mut xs, &mut ys);
    });
    Ok((PyArray1::from_vec(py, xs), PyArray1::from_vec(py, ys)))
}

macro_rules! converters {
    ($($(#[doc = $doc:literal])* $name:ident($x:ident, $y:ident) => $converter:path;)+) => {
        $(
            $(#[doc = $doc])*
            #[pyfunction]
            #[pyo3(signature = ($x, $y, /))]
            fn $name<'py>(
                $x: &Bound<'py, PyAny>,
                $y: &Bound<'py, PyAny>,
            ) -> PyResult<Converted<'py>> {
                convert($x, $y, $converter)
            }
        )+

        #[pymodule(gil_used = false)]
        mod cutil {
            $(
                #[pymodule_export]
                use super::$name;
            )+
        }
    };
}

converters! {
    /// Convert longitudes and latitudes to OSGB36 Eastings and Northings, using OSTN15 corrections.
    /// Returns a tuple of two float64 NumPy arrays: Eastings and Northings.
    convert_bng(longitudes, latitudes) => lonlat_bng::convert_to_bng_threaded_vec;
    /// Convert OSGB36 Eastings and Northings to longitudes and latitudes, using OSTN15 corrections.
    /// Returns a tuple of two float64 NumPy arrays: longitudes and latitudes.
    convert_lonlat(eastings, northings) => lonlat_bng::convert_to_lonlat_threaded_vec;
    /// Convert longitudes and latitudes to OSGB36 Eastings and Northings, using OSTN15 corrections.
    /// Returns a tuple of two float64 NumPy arrays: Eastings and Northings.
    convert_to_osgb36(longitudes, latitudes) => lonlat_bng::convert_to_osgb36_threaded_vec;
    /// Convert longitudes and latitudes to ETRS89 Eastings and Northings, without OSTN15 corrections.
    /// Returns a tuple of two float64 NumPy arrays: Eastings and Northings.
    convert_to_etrs89(longitudes, latitudes) => lonlat_bng::convert_to_etrs89_threaded_vec;
    /// Convert ETRS89 Eastings and Northings to OSGB36 Eastings and Northings, using OSTN15 corrections.
    /// Returns a tuple of two float64 NumPy arrays: Eastings and Northings.
    convert_etrs89_to_osgb36(eastings, northings) => lonlat_bng::convert_etrs89_to_osgb36_threaded_vec;
    /// Convert ETRS89 Eastings and Northings to longitudes and latitudes.
    /// Returns a tuple of two float64 NumPy arrays: longitudes and latitudes.
    convert_etrs89_to_ll(eastings, northings) => lonlat_bng::convert_etrs89_to_ll_threaded_vec;
    /// Convert OSGB36 Eastings and Northings to longitudes and latitudes, using OSTN15 corrections.
    /// Returns a tuple of two float64 NumPy arrays: longitudes and latitudes.
    convert_osgb36_to_ll(eastings, northings) => lonlat_bng::convert_osgb36_to_ll_threaded_vec;
    /// Convert OSGB36 Eastings and Northings to ETRS89 Eastings and Northings, using OSTN15 corrections.
    /// Returns a tuple of two float64 NumPy arrays: Eastings and Northings.
    convert_osgb36_to_etrs89(eastings, northings) => lonlat_bng::convert_osgb36_to_etrs89_threaded_vec;
    /// Convert Web Mercator (EPSG:3857) x and y coordinates to WGS84 longitudes and latitudes.
    /// Returns a tuple of two float64 NumPy arrays: longitudes and latitudes.
    convert_epsg3857_to_wgs84(x, y) => lonlat_bng::convert_epsg3857_to_wgs84_threaded_vec;
}
