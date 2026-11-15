after cloning, run:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Example usage:


# an example of how the library is intended to be used

import spherex_tools

# searching for observations around a location
observations = spherex_tools.search(
    ra=304.693508808,
    dec=42.4436872991
)

print("observations found:", len(observations))

# retrieving the first observation
if len(observations) > 0:

    cutout = spherex_tools.get_cutout(
        observations[0],
        ra=304.693508808,
        dec=42.4436872991
    )

    # opening the fits file and extracting its main image
    hdul = spherex_tools.open_fits(cutout)

    image = spherex_tools.get_image(hdul)

    print("image dimensions:", image.shape)

    hdul.close()
