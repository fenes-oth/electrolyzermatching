"""Load versioned, prebuilt electrolyzer datasets."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import pandas as pd
from platformdirs import user_cache_dir

DEFAULT_DATA_URL = (
    "https://raw.githubusercontent.com/fenes-oth/electrolyzermatching/"
    "v{version}/electrolyzers.csv"
)


def electrolyzers(
    *,
    from_url: bool = True,
    version: str = "0.2.0",
    path: str | Path | None = None,
    url: str | None = None,
    cache: bool = True,
) -> pd.DataFrame:
    """Load a prebuilt electrolyzer dataset as a pandas DataFrame.

    Args:
        from_url: Download the versioned dataset when ``True``.
        version: Dataset release version used by ``DEFAULT_DATA_URL``.
        path: Local CSV path. This is useful for offline and reproducible runs.
        url: Optional explicit CSV URL, useful for mirrors or development builds.
        cache: Cache downloaded data in the user cache directory.

    Raises:
        ValueError: If incompatible loading options are supplied.
        FileNotFoundError: If the requested local file does not exist.
        RuntimeError: If the remote dataset cannot be downloaded.
    """
    if path is not None and from_url:
        raise ValueError("Set from_url=False when loading a local path")

    if path is not None:
        local_path = Path(path)
        if not local_path.is_file():
            raise FileNotFoundError(local_path)
        return pd.read_csv(local_path)

    if not from_url:
        raise ValueError("Provide path when from_url=False")

    if "/" in version or "\\" in version:
        raise ValueError("version must be a simple release identifier")

    data_url = url or DEFAULT_DATA_URL.format(version=version)
    cache_path = Path(user_cache_dir("electrolyzermatching")) / (
        f"electrolyzers-{version}.csv"
    )

    if cache and cache_path.is_file():
        return pd.read_csv(cache_path)

    try:
        with urlopen(data_url) as response:
            content = response.read()
    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(f"Unable to download electrolyzer data from {data_url}") from error

    if cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = cache_path.with_suffix(".tmp")
        temporary_path.write_bytes(content)
        temporary_path.replace(cache_path)

    return pd.read_csv(BytesIO(content))
