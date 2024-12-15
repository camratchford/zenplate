# Building Zenplate

For convenience, each of these processes is scripted. These scripts can be found in the `extras/scripts` directory.

Before running the script ensure that the development dependencies are installed. This can be done by running the following command:

```shell
# From the root of the repository
pip install -e .[development]
```


## The documentation

The resulting documentation will be located in the `extras/docs/site` directory.

For POSIX:
    
```bash
./extras/scripts/mkdocs.sh
```

For Windows:

```powershell
.\extras\scripts\mkdocs.ps1
```

## The pyinstaller binary

The resulting binary will be located in the `dist` directory.

For POSIX:
    
```bash
./extras/scripts/pyinstaller.sh
```

For Windows:

```powershell
.\extras\scripts\pyinstaller.ps1
```
