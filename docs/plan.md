# ElectrolyzerMatching plan

## Data distribution decision

A xx MB `powerplants.csv`-style file is technically acceptable, but it should not be committed to the source package by default. A large tracked file increases clone size, slows package development, and couples data releases to code releases.

The project will use a hybrid approach:

- Keep a tiny, representative CSV fixture in the repository for tests and examples.
- Generate the complete matched dataset in a reproducible build job.
- Publish versioned CSV and Parquet artifacts as GitHub Release assets or to Zenodo.
- Load remote artifacts through `electrolyzermatching.electrolyzers()` and cache them under the platform user cache directory.
- Support an explicit local path for offline and fully reproducible analyses.
- Store a manifest beside each artifact with schema version, source versions, generation timestamp, row count, and checksums.

A checked-in 20 MB CSV can be acceptable for an early research prototype if the data is stable and licensing permits it. It should remain outside the Python wheel and should be moved to release assets when the dataset or contributor base grows.

## Implementation roadmap

1. **Prebuilt data loader**
   - Add `electrolyzers(from_url=True, version=...)`.
   - Support local paths, explicit URLs, caching, and useful download errors.
   - Establish the canonical column names and data versioning convention.

2. **Canonical schema and validation**
   - Define required electrolyzer fields and dtypes.
   - Validate duplicates, coordinates, capacities, statuses, and source provenance.
   - Add a small checked-in fixture and focused tests.

3. **Source adapters**
   - Add `electrolyzermatching.data.SourceName()` adapters.
   - Keep source-specific dependencies optional.
   - Normalize each source into the canonical schema before matching.

4. **Matching pipeline**
   - Add `combine(sources=..., config=...)`.
   - Separate normalization, candidate generation, scoring, and reconciliation.
   - Preserve source identifiers and match confidence in the output.

5. **Dataset build and release automation**
   - Add a dedicated workflow that fetches sources, runs the pipeline, validates outputs, and publishes artifacts.
   - Keep this separate from the PyPI package publishing workflow.
   - Produce CSV for inspection, Parquet for efficient loading, and a manifest for provenance.

6. **Documentation and compatibility**
   - Document the public API, schema, data sources, licenses, and reproducibility procedure.
   - Pin dataset versions in examples and analysis records.
   - Add integration tests against a local fixture and a release asset.
