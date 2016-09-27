import System.IO
import Data.Char
import System

usage = unlines [
        "Read map functions from a file and write them into a template"
       ,"for a map-reduce based design document for couchdb."
       ,"View names are formed from the file which is read in..."
       ,"Usage: <program> name-of-map-file"
       ,"   where the map-file contains a sequence of "
       ,"\"name\\n\" definition\\n ",""
       ,"More documentation: read the code."
        ]

main :: IO ()
main = do args <- getArgs
          if null args then putStrLn usage else do
          defs <- readFile (args!!0)
          let suffix = trim (args!!0)
              pairs = parse (lines defs)
              outname = args!!0 ++ ".view"
              out_id  = "_design/" ++ suffix
              outs = unlines $ 
                       (("{ \"_id\": " ++ show out_id ++ ",")
                        :"\"language\": \"javascript\","
                        :"\"views\": {"
                        : concatMap writeView pairs
                       ) ++ ["}","}"]
          writeFile outname outs

writeView :: (String,String) -> [String]
writeView (name,def) 
    = (show name ++ ": {")
       : ("\"map\": " ++ show def ++ ",")
       : ("\"reduce\": " ++ show std_reduce)
       : ["},"] 

std_reduce = unlines $ 
             [ "function(key,outs,rereduce) {"
             , "  result = {count:0,wall_duration:0,charge:0};"
             , "  for (o in outs) {"
             , "    result.count += (outs[o])[\"count\"];"
             , "    result.wall_duration += (outs[o])[\"wall_duration\"];"
             , "    result.charge += (outs[o]).charge;"
             , "  }"
             , "  return result;"
             , "}"
             ]

parse :: [String] -> [(String,String)]
parse [] = []
parse [x] | all isSpace x = []
          | otherwise = error $ "unmatched line content at the end:\n" ++ x
parse (n_:rest) -- entry: take a name (single word), then eat definition
    = let name        = trim n_
          (d1,r)     = break (=='{') (head rest)
          (d2,next)  = matchBraces 1 "{" (maybetail r:tail rest)
          maybetail [] = error $ "unexpected first line: " ++ head rest
          maybetail xs = tail xs
      in (name,d1 ++ d2) : parse next

matchBraces :: Int -> String -> [String] -> (String,[String])
matchBraces   0   acc rest = (reverse acc,rest)

matchBraces level acc [] = error 
        ("End reached, but bracket level /= 0.\nLevel:"
         ++ show level ++ '\n':(reverse acc))
matchBraces l acc ([]:rest) = matchBraces l ('\n':acc) rest
matchBraces level acc (line:rest) = 
    let (new_l,new_acc) = matchInLine level acc line
    in matchBraces new_l new_acc rest

matchInLine l acc ""  = (l,'\n':acc)
matchInLine l acc (c:rest) = matchInLine l' (c:acc) rest
    where l' | c == '{' = l+1
             | c == '}' = l-1
             | otherwise = l

trim :: String -> String
trim = reverse . (dropWhile isSpace) . reverse . (dropWhile isSpace)
