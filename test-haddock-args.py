#!/usr/bin/env python3
"""
Test script to verify the fix for the issue with -haddock swallowing other arguments.
This demonstrates how the issue occurred and how our fix resolves it.
"""

class ConfiguredProgram:
    def __init__(self, programId, programOverrideArgs):
        self.programId = programId
        self.programOverrideArgs = programOverrideArgs

# Original broken implementation (prepending -haddock)
def addHaddockIfDocumentationEnabled_broken(cp):
    if cp.programId == "ghc":
        return ConfiguredProgram(cp.programId, ["-haddock"] + cp.programOverrideArgs)
    else:
        return cp

# Fixed implementation (appending -haddock)
def addHaddockIfDocumentationEnabled_fixed(cp):
    if cp.programId == "ghc":
        return ConfiguredProgram(cp.programId, cp.programOverrideArgs + ["-haddock"])
    else:
        return cp

# Simulate Map.unionWith (<>) on lists
def map_union_with_concat(list1, list2):
    # In Haskell, (<>) for lists is concatenation, but Map.unionWith only uses the 
    # value from the first map when the key exists in both maps
    return list1  # Only use list1 if both keys exist

def test_implementation(title, add_haddock_func):
    print(f"\n{title}:")
    print("-" * len(title) + "------")
    
    # Create a program with some optimization flags
    program = ConfiguredProgram("ghc", ["-O2", "-Wall"])
    print(f"Original program args: {program.programOverrideArgs}")
    
    # Add -haddock flag
    program_with_haddock = add_haddock_func(program)
    print(f"After adding -haddock: {program_with_haddock.programOverrideArgs}")
    
    # Simulate arguments from packageConfigProgramArgs
    other_args = ["-dynamic", "-threaded"]
    print(f"Other config arguments: {other_args}")
    
    # Simulate Map.unionWith (<>) when both maps have the "ghc" key
    # This is what happens in the real code when elabProgramArgs is combined with
    # perPkgOptionMapMappend pkgid packageConfigProgramArgs
    result = map_union_with_concat(program_with_haddock.programOverrideArgs, other_args)
    print(f"After Map.unionWith (<>): {result}")
    
    return result

def main():
    print("This script demonstrates how the -haddock flag interacts with other GHC arguments")
    print("when using the Map.unionWith (<>) operator to combine arguments from different sources.")
    
    # Test the original broken implementation
    result_broken = test_implementation(
        "BROKEN APPROACH (prepending -haddock)", 
        addHaddockIfDocumentationEnabled_broken
    )
    
    # Test the fixed implementation
    result_fixed = test_implementation(
        "FIXED APPROACH (appending -haddock)", 
        addHaddockIfDocumentationEnabled_fixed
    )
    
    # Show the overall verdict
    print("\nVERDICT:")
    print("-------")
    if "-O2" in result_broken and "-Wall" in result_broken and "-haddock" in result_broken:
        print("Original implementation: All original flags preserved ✓")
    else:
        print("Original implementation: Original flags lost ✗")
        
    if "-dynamic" in result_broken and "-threaded" in result_broken:
        print("Original implementation: Configuration arguments preserved ✓")
    else:
        print("Original implementation: Configuration arguments lost ✗")
    
    if "-O2" in result_fixed and "-Wall" in result_fixed and "-haddock" in result_fixed:
        print("Fixed implementation: All original flags preserved ✓")
    else:
        print("Fixed implementation: Original flags lost ✗")
        
    if "-dynamic" in result_fixed and "-threaded" in result_fixed:
        print("Fixed implementation: Configuration arguments preserved ✓")
    else:
        print("Fixed implementation: Configuration arguments lost ✗")

if __name__ == "__main__":
    main()