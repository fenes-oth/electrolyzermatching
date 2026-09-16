# ElectrolyzerMatching

Matching and modeling algorithms for electrolyzer systems.

## Load the prebuilt dataset

Install the package, then load the versioned dataset online:

```python
import electrolyzermatching as em

plants = em.electrolyzers()
print(plants.head())
print(plants.columns)
```

The default dataset is pinned to version `0.2.0`. Downloads are cached in the
platform-specific user cache directory. A different tagged dataset or a
development URL can be selected explicitly:

```python
plants = em.electrolyzers(version="0.2.0", cache=False)
plants = em.electrolyzers(
	url="https://example.org/electrolyzers.csv",
	version="custom",
)
```

## Load custom data

Pass a local CSV path for custom or offline data. The CSV must have a header;
additional columns are preserved.

```python
custom = em.electrolyzers(
	from_url=False,
	path="my-electrolyzers.csv",
)
```

The included dataset currently contains `name`, `country`, and
`capacity_mw`. Standard pandas filtering and aggregation can be used after
loading:

```python
german = plants[plants["country"] == "DE"]
capacity = german.groupby("country")["capacity_mw"].sum()
```

## Development and testing

```bash
uv sync --group dev
uv run pytest
uv build
```

The tests do not require network access. Online loading is tested with a
mocked response; custom loading is tested against a temporary local CSV.
