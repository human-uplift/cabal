#!/bin/bash

# Exit on error
set -e

echo "Testing the fix for Cabal issue #10782 / #10783"
echo "================================================"
echo ""

# First clean any previous builds
rm -rf dist-newstyle
echo "1. Running command: cabal build --ghc-options=\"-Wall -Werror\" --enable-documentation"
cabal build --ghc-options="-Wall -Werror" --enable-documentation

# This should fail due to unused import
if [ $? -eq 0 ]; then
  echo "ERROR: Build should have failed with -Wall -Werror due to unused import!"
  exit 1
else
  echo "SUCCESS: Build correctly failed with -Wall -Werror as expected."
fi

echo ""
echo "Test passed: The --ghc-options are no longer swallowed by --enable-documentation"
exit 0
