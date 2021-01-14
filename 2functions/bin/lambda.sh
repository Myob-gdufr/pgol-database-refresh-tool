#!/bin/bash

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$( echo $BIN_DIR | sed -e 's/\/bin$//')"
INSTALL_DIR="/opt"
BUILD_DIR="/tmp/assemble_lambda"
export AWS_DEFAULT_REGION=ap-southeast-2

source "${BIN_DIR}/include/text.ext"
source "${BIN_DIR}/include/python_modules.ext"
source "${BIN_DIR}/include/yum_packages.ext"

#  These are the yum packages we need.
MODULES=("git" "python3")
ensure_yum_package_list_present "${MODULES[@]}"
if [ $? -ne 0 ]
then
  error "We cannot continue without these yum packages  ${MODULES} installed."
  exit -1
fi


declare USER_FLAG="--user"

#  First we need to make sure we have virtualenv installed.
MODULES=("virtualenv")
ensure_python_module_list_present "${MODULES[@]}"
if [ $? -ne 0 ]
then
  error "We cannot continue without these python modules ${MODULES}."
  exit -1
fi

unset USER_FLAG

# Now we need to verify that we have a virtual python environment
ensure_virtual_environment_present
if [ $? -ne 0 ]
then
  error "We cannot continue without having the virtual environment created."
  exit -1
fi

switch_to_virtual_environment
if [ $? -ne 0 ]
then
  error "We cannot continue without initializing the virtual environment."
  exit -1
fi

#  These are the modules we need in the virtual environment.
MODULES=("wheel")
ensure_python_module_list_present "${MODULES[@]}"
if [ $? -ne 0 ]
then
  error "We cannot continue without these python modules ${MODULES} inside the virtual environment."
  exit -1
fi

mkdir -m 777 -p "${BUILD_DIR}"

pushd "${ROOT_DIR}/src/rdsbackup"
rm -rf "${BUILD_DIR}/python"
pip install . -t "${BUILD_DIR}/python"
popd

pushd $BUILD_DIR
rm -rf /tmp/rds_lambda.zip
zip -r /tmp/rds_lambda.zip .
popd

aws s3 cp /tmp/rds_lambda.zip s3://myob-pgol-dev-artifacts/lambda/layers/rds.zip
aws lambda publish-layer-version --layer-name rds_lib --description "rds python library" --content S3Bucket=myob-pgol-dev-artifacts,S3Key=lambda/layers/rds.zip --compatible-runtimes python3.6 python3.7 python3.8

