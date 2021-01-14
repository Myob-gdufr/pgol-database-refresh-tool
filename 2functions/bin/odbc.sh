#!/bin/bash

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$( echo $BIN_DIR | sed -e 's/\/bin$//')"
INSTALL_DIR="/opt"
BUILD_DIR="/opt"
export AWS_DEFAULT_REGION=ap-southeast-2


source "${BIN_DIR}/include/ftp_downloads.ext"
source "${BIN_DIR}/include/text.ext"
source "${BIN_DIR}/include/yum_packages.ext"

#  These are the yum packages we need.
MODULES=("git" "gcc" "gcc-c++")
ensure_yum_package_list_present "${MODULES[@]}"
if [ $? -ne 0 ]
then
  error "We cannot continue without these yum packages  ${MODULES} installed."
  exit -1
fi

#  Now we process the third party packages
mkdir -m 0755 -p "${ROOT_DIR}/third-party"
sudo mkdir -p "${INSTALL_DIR}"
sudo chmod 0777 "${INSTALL_DIR}"

ensure_download_present "unixODBC" "ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.7.tar.gz"

pushd "${ROOT_DIR}/third-party/unixODBC"
./configure --disable-gui --disable-drivers --enable-iconv --with-iconv-char-enc=UTF8 --with-iconv-ucode-enc=UTF16LE  --prefix=$INSTALL_DIR
make install
popd

sudo bash -c 'curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/mssql-release.repo'
sudo ACCEPT_EULA=Y yum install -y msodbcsql17
sudo cp /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.6.so.1.1 /opt/lib/

#  Update the ini files.
cat <<EOF > $BUILD_DIR/etc/odbcinst.ini
[ODBC Drivers]
ODBC Driver 17 for SQL Server=Installed

[ODBC Driver 17 for SQL Server]
Description=Microsoft ODBC Driver 17 for SQL Server
Driver=${INSTALL_DIR}/lib/libmsodbcsql-17.6.so.1.1
EOF

cat <<EOF > $BUILD_DIR/etc/odbc.ini
[ODBC Driver 17 for SQL Server]
Driver      = ODBC Driver 17 for SQL Server
Description = My ODBC Driver 17 for SQL Server
Trace       = No
EOF

# Now grab the odbc layer for use later...
#tar -zcf /tmp/odbc_lambda.tar.gz -C /var/task .
pushd $BUILD_DIR
zip -r /tmp/odbc_lambda.zip bin etc lib share
popd

aws s3 cp /tmp/odbc_lambda.zip s3://myob-pgol-dev-artifacts/lambda/layers/odbc.zip
aws lambda publish-layer-version --layer-name mssql_driver --description "ODBC and SQL driver" --content S3Bucket=myob-pgol-dev-artifacts,S3Key=lambda/layers/odbc.zip --compatible-runtimes python3.6 python3.7 python3.8
