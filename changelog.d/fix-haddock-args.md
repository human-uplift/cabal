synopsis: Fixed a bug where enabling haddock swallowed other GHC options
description: |
  When building with both `--enable-documentation` and other GHC options like 
  `--ghc-options="-Wall -Werror"`, the GHC options were being ignored due to
  the way arguments were combined. This has been fixed by appending the haddock
  flag rather than prepending it.
significance: bugfix
