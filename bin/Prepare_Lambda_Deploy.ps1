install-package AWS.Tools.SecurityToken -Force
install-package AWS.Tools.EC2 -Force

pip install --upgrade aws-sam-cli
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

sam --version


