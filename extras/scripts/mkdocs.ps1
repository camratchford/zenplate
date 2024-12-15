$CurDir = Split-Path -path $(Get-Item -Path $MyInvocation.MyCommand.Source -ErrorAction Stop).FullName -Parent

Push-Location $CurDir

$DocsDir = "../docs/"

Push-Location $DocsDir
mkdocs build

Pop-Location
Pop-Location

