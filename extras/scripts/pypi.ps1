$CurDir = Split-Path -path $(Get-Item -Path $MyInvocation.MyCommand.Source -ErrorAction Stop).FullName -Parent
$RepoRoot = Split-Path (Split-Path -path $CurDir -Parent) -Parent
Push-Location $RepoRoot



Remove-Item -Recurse -Force sdist
New-Item -ItemType Directory -Force -Path sdist | Out-Null
python -m build --wheel --outdir sdist
python -m build --sdist --outdir sdist
twine upload --verbose --repository pypi sdist/*

Pop-Location