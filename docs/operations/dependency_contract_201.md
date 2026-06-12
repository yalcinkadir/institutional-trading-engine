# Dependency Contract #201

Status date: 2026-06-12

## Authoritative install source

`requirements.txt` is the authoritative install entry point for contributors and CI.

It delegates to the pinned lock file:

```text
-r requirements.lock
```

## Lock file

`requirements.lock` is the pinned dependency source.

It must contain exact pins only, for example:

```text
package==x.y.z
```

Floating comparators such as `>=`, `<=`, `~=`, `<` or `>` are not allowed in the lock contract.

## Contributor install command

```text
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## CI install command

The main CI workflow installs dependencies through:

```text
pip install -r requirements.txt
```

Because `requirements.txt` delegates to `requirements.lock`, CI and local contributors use the same pinned source.

## Security/dependency scan target

Dependency and security scans should target the authoritative install entry point:

```text
requirements.txt
```

Scanners that inspect lock files directly may additionally inspect:

```text
requirements.lock
```

but `requirements.lock` must not become a second, undocumented install entry point.

## Guard tests

```text
tests/test_sr8_dependency_reproducibility.py
tests/test_201_dependency_contract.py
```
