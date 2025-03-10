## Building notes

## Compile

```
cd src
./docker-setup.txt


# In docker image:

rm -rf */build-soh

git clone https://github.com/libsdl-org/SDL.git
cd SDL
git checkout release-2.32.0 # was 2.26.2
mkdir -p build-soh && cd build-soh
cmake ..
make -j8
make install
cd ../..

git clone https://github.com/libsdl-org/SDL_net.git
cd SDL_net
git checkout release-2.2.0
mkdir build-soh && cd build-soh
cmake ..
make -j8
make install
cd ../..

git clone https://github.com/nih-at/libzip.git
cd libzip
mkdir build-soh && cd build-soh
cmake ..
make -j8
make install
cd ../..

git clone https://github.com/nlohmann/json.git
cd json
mkdir build-soh && cd build-soh
cmake ..
make -j8
make install
cd ../..

git clone https://github.com/libarchive/bzip2.git
cd bzip2
mkdir build-soh && cd build-soh
cmake ..
make -j8
make install
cd ../..

git clone https://github.com/leethomason/tinyxml2.git
cd tinyxml2
git checkout .
mkdir build-soh && cd build-soh
cmake -DBUILD_SHARED_LIBS=ON ..
make -j8
make install

# prevent this file being found by cmake when SoH is compiled
cd ..
mv cmake/tinyxml2-config.cmake cmake/tinyxml2-config.cmake.disabled
cd ..

#### SoH ####
# need libglew-dev if compiling 8.0.6
git clone https://github.com/HarbourMasters/Shipwright.git
cd Shipwright
git submodule update --init
mkdir build-soh && cd build-soh
# -DBUILD_CROWD_CONTROL=0 no longer used in HEAD
CC=clang-18 CXX=clang++-18 cmake .. -GNinja -DUSE_OPENGLES=1 \
 -DCMAKE_BUILD_TYPE=Release
cmake --build . -j8

cmake --build . --target GenerateSohOtr -j8


# To retrieve build products to the host:

docker cp soh-build:/root/Shipwright/build-soh/soh/soh.elf .
docker cp soh-build:/root/Shipwright/build-soh/soh/soh.otr .
docker cp soh-build:/root/Shipwright/build-soh/ZAPD/ZAPD.out ./assets/

#### 2S2H ####

git clone https://github.com/HarbourMasters/2ship2harkinian.git
cd 2ship2harkinian
git checkout 1.1.2

# Clone the submodules
git submodule update --init

# Patch for old git
cd libultraship
patch -p1 < ../../soh2.patch
cd ..

mkdir build-soh && cd build-soh

CC=clang-18 CXX=clang++-18 cmake .. -GNinja -DUSE_OPENGLES=1 \
 -DBUILD_CROWD_CONTROL=0 -DCMAKE_BUILD_TYPE=Release
cmake --build . -j8

cmake --build . --target Generate2ShipOtr -j8


# To retrieve build products to the host:

docker cp soh-build:/root/2ship2harkinian/build-soh/mm/2s2h.elf .
docker cp soh-build:/root/2ship2harkinian/build-soh/mm/2ship.o2r .
docker cp soh-build:/root/2ship2harkinian/build-soh/ZAPD/ZAPD.out ./assets/extractor/
## FIXME: collate libraries to ./libs.2s2h.elf
docker cp soh-build:/root/Shipwright/build-soh/libs.2s2h.elf ./libs

```
