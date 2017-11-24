# Update & Upgrade The Ubuntu Packages
sudo apt-get -y update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade 
# Install Build Essential Tools & Headers
sudo apt-get -y install build-essential linux-headers-$(uname -r)  
sudo apt-get autoremove  
# Install Sleuthkit Dependencies
cd ~  
sudo apt-get install zlib1g-dev libssl-dev libncurses5-dev  
sudo apt-get install libcurl4-openssl-dev libexpat1-dev libreadline-gplv2-dev  
sudo apt-get install uuid-dev libfuse-dev bzip2 libbz2-dev git  
sudo apt-get -y install automake 
sudo apt-get -y install autoconf libtool  
# Install libewf
wget -v https://github.com/libyal/libewf/releases/download/20171104/libewf-experimental-20171104.tar.gz
tar -xvf libewf-experimental-20171104.tar.gz
cd libewf-20140608/  
./configure  
make  
sudo make install 
# Install AFFLIB
cd ~  
git clone git://github.com/simsong/AFFLIBv3.git  
cd AFFLIBv3/  
./bootstrap.sh  
./configure  
make  
sudo make install  
# Install Sleuthkit
cd ~  
git clone git://github.com/sleuthkit/sleuthkit.git  
cd sleuthkit  
./bootstrap  
./configure  
make  
sudo make install
# install autopsy
cd ~
mkdir evidence_locker  
git clone -b autopsy-2 git://github.com/sleuthkit/autopsy.git  
cd autopsy
./configure
#