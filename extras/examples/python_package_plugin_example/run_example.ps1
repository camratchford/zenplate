$CurDir = Split-Path -path $MyInvocation.MyCommand.Source -Parent
Push-Location $CurDir

zenplate.exe --var-file vars/vars.yml `
        --force `
        templates output_dir

Pop-Location