#!/usr/bin/env python3

# This script demonstrates the issue #10782 and how the fix resolves it
# by simulating the behavior of the Flag Semigroup instance and the 
# argument merging logic

class Flag:
    """Simulates the Haskell Flag type and its Semigroup instance"""
    def __init__(self, value=None):
        self.value = value
        
    def combine_before_fix(self, other):
        """Before fix: left-biased combination"""
        if self.value is not None:
            return Flag(self.value)
        return other
    
    def combine_after_fix(self, other):
        """After fix: right-biased combination (reversed order)"""
        if other.value is not None:
            return Flag(other.value)
        return self
        
    def __str__(self):
        if self.value is None:
            return "NoFlag"
        return f"Flag({self.value})"

def simulate_before_fix(default_value, cmd_line_value):
    """Simulate the behavior before the fix"""
    default_flag = Flag(default_value)
    cmd_line_flag = Flag(cmd_line_value)
    
    # Before fix, we combine in the wrong order: default <> cmd_line 
    # This means default takes precedence
    result = default_flag.combine_before_fix(cmd_line_flag)
    return result

def simulate_after_fix(default_value, cmd_line_value):
    """Simulate the behavior after the fix"""
    default_flag = Flag(default_value)
    cmd_line_flag = Flag(cmd_line_value)
    
    # After fix, we combine in the correct order: cmd_line <> default
    # This means command line arguments take precedence
    result = cmd_line_flag.combine_before_fix(default_flag)
    return result

# Test case 1: Default value is set, command line value is set
print("Test Case 1: Default has value, command line has value")
print("  Default value: default.cabal")
print("  Command line value: example.cabal")
print("  Before fix:", simulate_before_fix("default.cabal", "example.cabal"))
print("  After fix:", simulate_after_fix("default.cabal", "example.cabal"))
print()

# Test case 2: Default value is set, command line value is not set
print("Test Case 2: Default has value, command line has no value")
print("  Default value: default.cabal")
print("  Command line value: None")
print("  Before fix:", simulate_before_fix("default.cabal", None))
print("  After fix:", simulate_after_fix("default.cabal", None))
print()

# Test case 3: Default value is not set, command line value is set
print("Test Case 3: Default has no value, command line has value")
print("  Default value: None")
print("  Command line value: example.cabal")
print("  Before fix:", simulate_before_fix(None, "example.cabal"))
print("  After fix:", simulate_after_fix(None, "example.cabal"))
print()

print("Conclusion: The fix ensures that command-line arguments take precedence over default values,")
print("which solves the issue where -haddock was swallowing other arguments like --cabal-file.")