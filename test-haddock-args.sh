#!/bin/bash
set -e

# Test script to verify the -haddock argument doesn't swallow other arguments
echo "Testing haddock arguments fix"

cd /cabal

# Create a temporary project
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

# Create a simple Cabal project
mkdir -p $TEMP_DIR/haddock-test
cd $TEMP_DIR/haddock-test

cat > haddock-test.cabal << EOF
cabal-version:      2.4
name:               haddock-test
version:            0.1.0.0
author:             Test
maintainer:         test@example.com
build-type:         Simple

library
  exposed-modules:    MyLib
  build-depends:      base >=4.13 && <5
  hs-source-dirs:     src
  default-language:   Haskell2010
EOF

mkdir -p src
cat > src/MyLib.hs << EOF
module MyLib where

-- | A test function
myFunc :: IO ()
myFunc = putStrLn "Hello, world!"
EOF

cat > cabal.project << EOF
packages: .
package haddock-test
  documentation: True
  ghc-options: -O2
EOF

# Build the project with our modified cabal
echo "Building the test project..."
/cabal/dist-newstyle/build/x86_64-linux/ghc-8.10.7/cabal-install-3.10.1.0/x/cabal/build/cabal/cabal v2-build --dry-run -v3 > build_log.txt 2>&1

# Check if both -haddock and -O2 arguments appear in the GHC command line
if grep -q -- "-haddock" build_log.txt && grep -q -- "-O2" build_log.txt; then
  echo "SUCCESS: Both -haddock and -O2 arguments are present"
  echo "Arguments test passed!"
  exit 0
else
  echo "FAILURE: One or both arguments missing"
  echo "Contents of build_log.txt:"
  cat build_log.txt
  exit 1
fi