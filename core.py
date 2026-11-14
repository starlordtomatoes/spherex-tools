
# spherex-tools
# a small python library for accessing spherex observations
#
# the goal is to make common archive operations easier to use
# without having to manually handle every archive request

import requests
import numpy as np

from io import BytesIO

from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.io import fits


def search(ra, dec, radius=1):
    # ra and dec point towards a location in the sky
    # radius controls how far around that location the search extends

    coord = SkyCoord(ra, dec, unit="deg")

    # querying the public spherex collection through irsa
    results = Irsa.query_sia(
        pos=(coord, radius * u.arcsec),
        collection="spherex_qr2"
    )

    return results


def get_cutout(observation, ra, dec, size=0.05):
    # an observation contains an access_url pointing to its fits file
    # the archive can return a smaller image around the requested coordinates

    access_url = observation["access_url"]

    cutout_url = (
        f"{access_url}"
        f"?center={ra},{dec}"
        f"&size={size}"
    )

    response = requests.get(cutout_url, timeout=120)

    # an unsuccessful download shouldn't silently produce a broken fits file
    response.raise_for_status()

    return response.content


def open_fits(data):
    # accepts the downloaded bytes and opens them as a fits file
    # BytesIO lets astropy read the data without saving a temporary file

    if isinstance(data, bytes):
        data = BytesIO(data)

    hdul = fits.open(data)

    return hdul


def get_image(hdul, product="IMAGE"):
    # retrieve a particular data product from the fits file
    # IMAGE is the default, but FLAGS, VARIANCE and ZODI may also be available

    if product not in hdul:
        raise ValueError(f"{product} is not available in this fits file")

    image = hdul[product].data

    if image is None:
        raise ValueError(f"{product} contains no image data")

    return np.asarray(image)
