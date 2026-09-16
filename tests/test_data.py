from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from electrolyzermatching.data import DEFAULT_DATA_URL, electrolyzers


def test_loads_custom_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "custom.csv"
    csv_path.write_text("name,country,capacity_mw\nCustom,DE,12\n")

    result = electrolyzers(from_url=False, path=csv_path)

    pd.testing.assert_frame_equal(
        result,
        pd.DataFrame(
            {"name": ["Custom"], "country": ["DE"], "capacity_mw": [12]}
        ),
    )


def test_downloads_versioned_csv_without_cache() -> None:
    response = MagicMock()
    response.read.return_value = b"name,country,capacity_mw\nOnline,FR,20\n"
    response.__enter__.return_value = response

    with patch("electrolyzermatching.data.urlopen", return_value=response) as open_url:
        result = electrolyzers(cache=False)

    open_url.assert_called_once_with(DEFAULT_DATA_URL.format(version="0.2.0"))
    assert result.to_dict("records") == [
        {"name": "Online", "country": "FR", "capacity_mw": 20}
    ]


def test_reuses_cached_download(tmp_path: Path) -> None:
    cache_path = tmp_path / "electrolyzers-0.2.0.csv"
    cache_path.write_text("name,country,capacity_mw\nCached,NL,30\n")

    with patch("electrolyzermatching.data.user_cache_dir", return_value=tmp_path):
        with patch("electrolyzermatching.data.urlopen") as open_url:
            result = electrolyzers()

    open_url.assert_not_called()
    assert result.iloc[0]["name"] == "Cached"


def test_rejects_local_path_with_url_mode(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="from_url=False"):
        electrolyzers(path=tmp_path / "custom.csv")