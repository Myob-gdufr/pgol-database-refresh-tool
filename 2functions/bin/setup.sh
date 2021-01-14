#!/bin/bash

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$( echo $BIN_DIR | sed -e 's/\/bin$//')"
source "${BIN_DIR}/include/ftp_downloads.ext"
source "${BIN_DIR}/include/text.ext"
source "${BIN_DIR}/include/python_modules.ext"

notice "Running the setup script for the RDS database backup process."

#  First we need to make sure we have virtualenv installed.
MODULES=("virtualenv")
ensure_python_module_list_present "${MODULES[@]}"
if [ $? -ne 0 ]
then
  error "We cannot continue without these python modules ${MODULES}."
  exit -1
fi

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
MODULES=("pyodbc" "wheel" "boto3")
ensure_python_module_list_present "${MODULES[@]}"
if [ $? -ne 0 ]
then
  error "We cannot continue without these python modules ${MODULES} inside the virtual environment."
  exit -1
fi
