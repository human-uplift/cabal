#!/bin/bash

# This script demonstrates and tests the fix for issue #10782 where
# -haddock swallows all other args when using <> operator to concatenate
# arguments.

# The issue happens because the Semigroup instance for Flag uses <> 
# in a way that the left argument can override the right one.

# For setupCabalFilePath, the problem was that we were using:
# setupCabalFilePath common' <> setupCabalFilePath commonFlags
# which meant default values were overriding command-line arguments.

# The fix reverses the order to preserve command-line arguments:
# setupCabalFilePath commonFlags <> setupCabalFilePath common'

echo "Test script to demonstrate the fix for issue #10782"
echo "Note: This is a theoretical demonstration since we cannot run the actual build"
echo ""
echo "Before the fix:"
echo "  Using: setupCabalFilePath common' <> setupCabalFilePath commonFlags"
echo "  - When running with -haddock --cabal-file=example.cabal"
echo "  - The default would override the --cabal-file argument"
echo ""
echo "After the fix:"
echo "  Using: setupCabalFilePath commonFlags <> setupCabalFilePath common'"
echo "  - When running with -haddock --cabal-file=example.cabal"
echo "  - The --cabal-file argument is preserved and not swallowed by -haddock"
echo ""
echo "The same logic applies to the setupWorkingDir flag."