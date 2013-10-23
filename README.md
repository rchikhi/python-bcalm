python-bcalm
============

Python implementation of the BCALM algorithm.

For better performance you should use the C++ version at https://github.com/Malfoy/bcalm

This implementation still uses a hash function to order minimizers. We now know this is sub-optimal.

Of independent interest, the file `ograph.py` implements a bidirected de Bruijn graph construction, with nodes compaction. See `main.py` for an example usage.
