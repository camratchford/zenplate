$CurDir = Split-Path -path $(Get-Item -Path $MyInvocation.MyCommand.Source -ErrorAction Stop).FullName -Parent
Push-Location $CurDir

zenplate.exe --var-file vars/specific_vars.yml `
        --var-file vars/general_vars.yml `
        --force `
        templates output_dir

Pop-Location