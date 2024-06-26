# Tests

To run the tests use the following command

```sh
python -mdoctest -v -f hw/*.py
```

or with `pytest` (you need `poetry` first)

```sh
poetry install
poetry run pytest -vx --doctest-modules
```
