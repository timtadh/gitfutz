Installing
==========

This isn't so much an install document for `gitfutz` as an install documents for
all the dependencies. `gitfutz` is not an "installable" thing yet so this is to
get you setup for hacking on it. The main dependency is `pygit2`. Unfortunately,
`pygit2` requires a c library `libgit2` to build.

I use [swork](https://github.com/timtadh/swork) to manage my shell enviroment. I
recommend you do the same when hacking (or at least installing) this project. It
should work fine if you use the `bash` shell and I can probably fix it up for
`zsh` as well.

Initial Setup
=============

get the code

    $ git clone https://timtadh@github.com/timtadh/gitfutz.git
    $ cd gitfutz

create a virtualenv

    $ virtualenv --no-site-packages env

add the project to swork

    $ sw add gitfutz
    $ sw start gitfutz


Install C Dependencies
======================

See the `c_requirements.md` document.


Install Python Dependencies
===========================

Make sure you start the project first (`sw start gitfutz`) if you haven't
already.

    $ cat python_requirements.txt | xargs pip install


What to do if you don't have swork
==================================

You may have chosen not to install `swork` or it is not working for you. If this
is the case when I say `sw start gitfutz` do the following:

    $ cd to the project root
    $ export SW_PROJECT_ROOT=`pwd`
    $ source .swork.activate

This will pollute your shell enivorment variables. To clean them up, simply
close the current shell and start a new one.

