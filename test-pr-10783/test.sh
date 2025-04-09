#!/bin/bash
set -e
echo "Testing whether -Wall -Werror flags work with documentation enabled..."
cd "$(dirname "$0")"

# First, let's demonstrate that the build should fail with -Wall -Werror due to the redundant import
if cabal run --ghc-options="-Wall -Werror" cabal-test > /dev/null 2>&1; then
  echo "ERROR: Build succeeded when it should have failed due to redundant import with -Wall -Werror"
  exit 1
else
  echo "✓ Good! Build failed as expected with -Wall -Werror"
fi

# Now, let's verify that with --enable-documentation, the -Wall -Werror flags still work
if cabal run --ghc-options="-Wall -Werror" --enable-documentation cabal-test > /dev/null 2>&1; then
  echo "ERROR: Build succeeded when it should have failed due to redundant import with -Wall -Werror and --enable-documentation"
  exit 1
else
  echo "✓ Good! Build failed as expected with -Wall -Werror and --enable-documentation"
  echo "This confirms the fix for issue #10782 works correctly!"
fi

echo "All tests passed!"
