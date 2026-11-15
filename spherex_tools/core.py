
"""Helpers for querying and inspecting SPHEREx observations from the IRSA archive."""

import requests
import numpy as np

from io import BytesIO

from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.io import fits


def search(ra, dec, radius=1):
    """Search the SPHEREx archive for observations near a sky position.

    Args:
        ra: Right ascension in degrees.
        dec: Declination in degrees.
        radius: Search radius in arcseconds.

    Returns:
        A query result table from astroquery's IRSA SIA service.
    """
    coord = SkyCoord(ra, dec, unit="deg")

    results = Irsa.query_sia(
        pos=(coord, radius * u.arcsec),
        collection="spherex_qr2"
    )

    return results


def get_cutout(observation, ra, dec, size=0.05):
    """Download a FITS cutout around a target coordinate.

    Args:
        observation: A row from a search result containing an ``access_url``.
        ra: Right ascension in degrees for the cutout center.
        dec: Declination in degrees for the cutout center.
        size: Desired cutout size in degrees.

    Returns:
        The raw FITS file content as bytes.
    """
    access_url = observation["access_url"]

    cutout_url = (
        f"{access_url}"
        f"?center={ra},{dec}"
        f"&size={size}"
    )

    response = requests.get(cutout_url, timeout=120)
    response.raise_for_status()

    return response.content


def open_fits(data):
    """Open a FITS file from bytes or a file-like object.

    Args:
        data: FITS bytes or a readable file-like object.

    Returns:
        An ``astropy.io.fits.HDUList`` instance.
    """
    if isinstance(data, bytes):
        data = BytesIO(data)

    hdul = fits.open(data)

    return hdul


def get_image(hdul, product="IMAGE"):
    """Read a named image product from a FITS file.

    Args:
        hdul: An HDU list returned by ``open_fits``.
        product: FITS extension name to read. Defaults to ``"IMAGE"``.

    Returns:
        A NumPy array for the selected data product.

    Raises:
        ValueError: If the requested product is missing or empty.
    """
    if product not in hdul:
        raise ValueError(f"{product} is not available in this fits file")

    image = hdul[product].data

    if image is None:
        raise ValueError(f"{product} contains no image data")

    return np.asarray(image)
