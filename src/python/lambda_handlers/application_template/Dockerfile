# This Dockerfile uses the aws lambda python3.8 image as a basis and
# installs all needed libraries for pyodbc (SQL server database interaction)

# Grab a fresh copy of the image and install dependencies
FROM public.ecr.aws/lambda/python:3.8

# Install build dependencies TODO: doesn't need all these, remove unnecessary 
RUN  ACCEPT_EULA=Y yum -y install \
    build-base \
    libtool \
    libtool-ltdl \
    autoconf \
    automake \
    libexecinfo-dev \
    make \
    cmake \
    libcurl \
    which \
    wheel \
    curl \
    gcc-c++

# clean up conflicting modules
RUN yum remove unixODBC-utf16-2.3.1-1.x86_64 unixODBC-2.3.7-1.rh.x86_64 unixODBC-utf16-2.3.1-1.x86_64

# add required microsoft package manager 
RUN curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo

# install pyodbc dependencies for ms sql interaction
RUN ACCEPT_EULA=Y yum -y install msodbcsql mssql-tools unixODBC-devel

# Install pyodbc
RUN python -m pip install pyodbc

# Copy the application files into the image
COPY app/   ./

# Set the entry point for AWS lambda execution
CMD ["lambda_function.lambda_handler"]