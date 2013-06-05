The C Requirements
==================

I assume you are using [swork](https://github.com/timtadh/swork) if you are not please do the following:

    $ export SW_PROJECT_ROOT= # the checkout root for gitfutz

libgit2
=======

##### url:
https://github.com/libgit2/libgit2

##### what:
the git library pygit2 uses

##### dependencies:
cmake

##### install:

0. cd to the checkout root of the gitfutz
1.  `$ sw add gitfutz` # Note: accept the premade files
                       # if you have already done this simply
                       # $ sw start -c gitfutz
                       # instead.
2.  install cmake
      - if on ubuntu, `$ sudo apt-get install cmake`
3.  `$ mkdir -p cdeps/srcs`
4.  `$ cd cdeps/srcs`
5.  `$ git clone https://github.com/libgit2/libgit2.git`
6.  `$ cd libgit2`
7.  `$ git checkout master` # important step! pygit2 relies on master not the
                            # default "development" branch.
8.  `$ mkdir build && cd build`
9.  `$ cmake .. -DCMAKE_INSTALL_PREFIX=$SW_PROJECT_ROOT/cdeps`
10. `$ cmake --build . --target install`

