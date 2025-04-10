#!/bin/bash
set -e

# Make sure we're in the right directory
cd "$(dirname "$0")"

echo "Testing the fix for --enable-documentation swallowing GHC options"
echo "----------------------------------------------------------------"

# First compile with Cabal, expecting failure due to -Wall -Werror and the redundant import
echo "Running: cabal run --ghc-options=\"-Wall -Werror\" --enable-documentation"
if cabal run --ghc-options="-Wall -Werror" --enable-documentation; then
  echo "ERROR: Build succeeded but should have failed due to -Wall -Werror and the redundant import"
  exit 1
else
  echo "SUCCESS: Build failed as expected with -Wall -Werror and --enable-documentation"
  echo "This confirms that --enable-documentation is correctly preserving other GHC options"
fi

echo "Test passed successfully!"
exit 0
