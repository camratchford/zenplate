$CurDir = Split-Path -path $MyInvocation.MyCommand.Source -Parent
Push-Location $CurDir

zenplate.exe --config-file config.yml `
        --force `
        templates output_dir

Pop-Location