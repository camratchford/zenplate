$CurDir = Split-Path -path $(Get-Item -Path $MyInvocation.MyCommand.Source -ErrorAction Stop).FullName -Parent
Push-Location $CurDir

zenplate.exe `
        -v 'title=How do you make a cheeseburger?' `
        --var-file 'vars/vars.yml' `
        --force `
        'templates/readme_template.md.j2' 'output_files/README.md'


Pop-Location