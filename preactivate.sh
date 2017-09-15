ROOT_DIR=`pwd`
PY_DIR=${ROOT_DIR}/.python
SSL_DIR=${ROOT_DIR}/.ssl
TMP_DIR=${ROOT_DIR}/.tmp

mkdir ${PY_DIR}
mkdir ${SSL_DIR}
mkdir ${TMP_DIR}

## Install OpenSSL
cd ${TMP_DIR}
wget http://www.openssl.org/source/openssl-1.0.2e.tar.gz
tar -zxf openssl-1.0.2e.tar.gz
cd ${TMP_DIR}/openssl-1.0.2e
./config --prefix=${SSL_DIR} --openssldir=${SSL_DIR}
make
make install

## Install Python2.7
cd ${TMP_DIR}
wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
tar -zxf Python-2.7.13.tgz
cd ${TMP_DIR}/Python-2.7.13
./configure --prefix=${PY_DIR}
make
echo "_ssl _ssl.c -DUSE_SSL -I${SSL_DIR}/include -I${SSL_DIR}/include/openssl -L${SSL_DIR}/lib -lssl -lcrypto" >> "${TMP_DIR}/Python-2.7.13/Modules/Setup"
make install

## Install virtualenv
cd ${TMP_DIR}
wget https://pypi.python.org/packages/d4/0c/9840c08189e030873387a73b90ada981885010dd9aea134d6de30cd24cb8/virtualenv-15.1.0.tar.gz#md5=44e19f4134906fe2d75124427dc9b716
tar -zxf virtualenv-15.1.0.tar.gz
cd ${TMP_DIR}/virtualenv-15.1.0/
${PY_DIR}/bin/python setup.py install

## Create a virtualenv with necessary dependencies
cd ${ROOT_DIR}
${PY_DIR}/bin/virtualenv env --python=${PY_DIR}/bin/python2.7
env/bin/pip install flask
env/bin/pip install mongokit
env/bin/pip install -I pymongo==2.8

## Delete .tmp
rm -r .tmp
