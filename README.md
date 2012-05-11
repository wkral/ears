ears
====

Listen for file changes and execute commands


About
-----

Instead of watching for file changes in a directory ears will run a server and
listen for changes sent by a text editor of IDE.

You can configure ears such that if a particular file pattern is matched a
particular command will be executed.

This is being built to replace [Nosy](http://github.com/wkral/Nosy) which
watches for file changes by stating all the files in a directory and performing
a check sum. This approach should use a lot less CPU and disk IO.


Editor Support
--------------

Vim: [http://github.com/wkral/ears-vim](http://github.com/wkral/ears-vim)


Protocol
--------

The protocol is trivial just connect to the ears server and write the full path
of a file that has been changed and ears will do the rest.
