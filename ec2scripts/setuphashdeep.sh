git clone https://github.com/jessek/hashdeep.git
cd hashdeep/
sudo apt-get install autotools-dev
sudo apt-get install automake
sudo apt-get install gcc-4.8 g++-4.8
sudo ./bootstrap.sh
sudo ./configure
sudo make
sudo make install
