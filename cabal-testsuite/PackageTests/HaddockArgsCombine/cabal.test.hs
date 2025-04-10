import Test.Cabal.Prelude

main = cabalTest $ do
    -- This command should fail with warnings because we have a redundant import
    -- and -Wall -Werror is specified, proving our fix works
    fails $ cabal "run" ["--ghc-options=-Wall -Werror", "--enable-documentation"]
