gitfutz
=======

This repos is for me to test ideas out for analyzing git repositories. I am
using the python libgit2 bindings as provided by pygit2.

Initial Questions
=================

I want to see if I can answer the following questions:

- What is the developer heirarchy?

  The merge information may provide insight into the social structure of the
  project. I want to see if it does for some (manually) selected github
  projects.

- Volatile vs Non-Volatile lines.

  I want to be able to identitfy for a range of commits (or times) what lines
  are considered "volatile" lines and what lines are considered "stable."

- Volatile vs Non-Volatile code structures.

  Same things as lines except look at specific code structures. I will probably
  use an AST representation of the code for this but a flow graph might also
  work.

There are lots of other questions to ask but these seem to be good ones to start
with. The volatile vs non-volatile [lines|stuctures] in particular leads
questions about those types of [lines|structures]. For instance one would like
to know if a non-volatile block is dead or not. This would require dead code
analysis. Another simple question, given a non-volatile block do any tests in
the test suite cover it? Do block stabilize (become non-volatile) before or
after a test suite covers the block?

