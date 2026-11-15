# spherex-tools

A small Python helper library for working with public SPHEREx observations provided through the IRSA archive.

The package wraps a few commonly used archive steps into a simple interface:

- search for observations near a sky position
- download a cutout around a target coordinate
- open the FITS file content
- read a specific image array from the FITS HDU

## Installation

Clone the repository and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Package layout

The public API is exposed from the top-level package:

```python
import spherex_tools
```

Available functions:

- `spherex_tools.search(ra, dec, radius=1)`
- `spherex_tools.get_cutout(observation, ra, dec, size=0.05)`
- `spherex_tools.open_fits(data)`
- `spherex_tools.get_image(hdul, product="IMAGE")`

## Quick start

```python
import spherex_tools

ra = 304.693508808
dec = 42.4436872991

# Find SPHEREx observations near the requested position.
observations = spherex_tools.search(ra=ra, dec=dec, radius=1)
print("observations found:", len(observations))

# Download a cutout around the first observation.
if len(observations) > 0:
    cutout = spherex_tools.get_cutout(
        observations[0],
        ra=ra,
        dec=dec,
        size=0.05,
    )

    hdul = spherex_tools.open_fits(cutout)
    image = spherex_tools.get_image(hdul)

    print("image dimensions:", image.shape)
    hdul.close()
```

## API reference

### `search(ra, dec, radius=1)`

Search the IRSA SPHEREx archive for observations near a position.

Parameters:

- `ra`: Right ascension in degrees
- `dec`: Declination in degrees
- `radius`: Search radius in arcseconds. The default value is `1`.

Returns:

- A table-like result set returned by `astroquery.ipac.irsa.Irsa.query_sia`.

This function creates a `SkyCoord` from the input coordinates and queries the `spherex_qr2` collection.

### `get_cutout(observation, ra, dec, size=0.05)`

Download a FITS cutout image for a specific observation.

Parameters:

- `observation`: A row from the archive search results. The function reads the `access_url` field.
- `ra`: Target right ascension in degrees
- `dec`: Target declination in degrees
- `size`: Desired cutout size in degrees. The default is `0.05`.

Returns:

- Raw FITS file bytes as a Python `bytes` object.

The underlying archive URL is constructed as:

```python
"{access_url}?center={ra},{dec}&size={size}"
```

### `open_fits(data)`

Open a FITS file from either raw bytes or an already opened file-like object.

Parameters:

- `data`: A `bytes` object or file-like object that can be read by `astropy.io.fits`

Returns:

- An `astropy.io.fits.HDUList` object.

### `get_image(hdul, product="IMAGE")`

Read a named image array from the FITS file.

Parameters:

- `hdul`: An `HDUList` returned by `open_fits`
- `product`: FITS extension name to read. Default is `"IMAGE"`.

Returns:

- A NumPy array containing the image data.

Raises:

- `ValueError` if the requested FITS product is absent or contains no data.

## Notes

- The library expects coordinates in degrees.
- The search radius is passed in arcseconds and is converted internally using `astropy.units.arcsec`.
- FITS downloads are checked with `response.raise_for_status()` so HTTP errors fail early instead of silently returning invalid data.
- This package is intentionally lightweight and targets the most common SPHEREx archive workflow rather than every possible archive operation.

## Dependencies

The project relies on:

- `astroquery`
- `astropy`
- `requests`
- `numpy`

