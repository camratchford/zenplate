$CurDir = Split-Path -path $(Get-Item -Path $MyInvocation.MyCommand.Source -ErrorAction Stop).FullName -Parent
$RepoRoot = Split-Path (Split-Path -path $CurDir -Parent) -Parent


pyinstaller -y --clean --console --onefile --uac-admin `
    --name "zenplate" `
    --paths "zenplate" `
    --icon "$CurDir/icon/zenplate.ico" `
    --log-level "FATAL" `
    --specpath "$RepoRoot/build" `
    "$RepoRoot/zenplate/cli.py"

