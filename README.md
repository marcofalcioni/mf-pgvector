# Docker
The docker file uses `postgres:latest` and builds the pgvector extension in place.  
The extension is automatically activated using an `init.sql` script.

Use `docker compose` to run the image.

# Poetry
This project uses poetry to manage python dependencies. 
Run `poetry install` and `poetry shell` to get a local virtual environment and activate it.

# Examples

Several examples of using `pgvector` are in the [examples](examples) folder.

## Molecule featurizer

Assume we have a db of molecules in a file `molecules.csv` - one SMILES per row.

To run the example:

```
docker compose up
poetry install
poetry shell
cd examples
python chem-feature.py <query_molecules> molecules.csv

```

The query molecule is a SMILES string, e.g. `c1ccco1`.

