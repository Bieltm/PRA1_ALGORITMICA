import Data.Foldable (foldl')
import Data.List (permutations)

type Pos = (Int, Int)
type Direccio = Char
type Graella  = [[Char]]

moviment :: Direccio -> (Int, Int)
moviment 'N' = (-1, 0)
moviment 'S' = ( 1, 0)
moviment 'E' = ( 0, 1)
moviment 'O' = ( 0,-1)
moviment  _  = ( 0, 0)   -- per seguretat

nextPos :: Pos -> Direccio -> Pos
nextPos (r, c) d =
    let (dr, dc) = moviment d
    in (r + dr, c + dc)

-- Llista de direccions base
direccions = ['N','S','E','O']

-- Possibles configuracions des de la posició actual i direcció donada
possibleConfigs :: Graella -> Pos -> Direccio -> [[Direccio]]
possibleConfigs graella pos dReal =
    filter (esPermutacioValida graella pos dReal) (permutations direccions)

-- Una permutació és vàlida si la seva primera direcció practicable coincideix amb la direcció donada
esPermutacioValida :: Graella -> Pos -> Direccio -> [Direccio] -> Bool
esPermutacioValida graella pos direccio perm =
    case primeraPracticable graella pos perm of
        Just d  -> d == direccio
        Nothing -> False

-- Troba la primera direcció practicable d'una permutació
primeraPracticable :: Graella -> Pos -> [Direccio] -> Maybe Direccio
primeraPracticable graella pos permutacio =
    case filter practicable permutacio of
        []    -> Nothing
        (d:_) -> Just d
  where
    practicable d =
        let pos' = nextPos pos d
        in esValid pos' && esLliure pos'

    esValid (r,c) =
        r >= 0 && r < length graella &&
        c >= 0 && c < length (head graella)

    esLliure (r, c) = graella !! r !! c /= '#'


-- Algorisme principal (extreure definició per a alumnes)

hits :: Graella -> [Direccio] -> Pos -> Maybe [Direccio] -> Int
hits graella recorregut posInicial _ = 
    let
        -- Generamos todas las permutaciones posibles una sola vez
        totesLesPerms = permutations direccions
        
        -- Estado: (Mapa de permutaciones validas -> coste mínimo para llegar a ella)
        -- Inicialmente, todas las permutaciones tienen coste 0
        estatInicial = map (\p -> (p, 0)) totesLesPerms

        -- Función auxiliar para procesar cada movimiento del rover
        processarMoviment (estatActual, pos) dReal =
            let
                -- 1. Calculamos la nueva posición tras el movimiento real
                novaPos = nextPos pos dReal
                
                -- 2. Filtramos qué permutaciones de las 24 totales son coherentes con dReal
                permsCoherents = filter (esPermutacioValida graella pos dReal) totesLesPerms
                
                -- 3. Calculamos el nuevo coste para cada permutación coherente
                nouEstat = map (\pNet -> 
                    let
                        costes = map (\(pAnt, cAnt) ->
                            if pAnt == pNet 
                            then cAnt        -- No hay rayo si mantenemos la misma
                            else cAnt + 1    -- Hay un rayo si cambiamos
                            ) estatActual
                    in (pNet, minimum costes)
                    ) permsCoherents
            in (nouEstat, novaPos)

        -- Aplicamos un foldl' para recorrer todo el camino del rover
        (estatFinal, _) = foldl' processarMoviment (estatInicial, posInicial) recorregut

    in if null estatFinal then 0 else minimum (map snd estatFinal)

-- Funció principal
main :: IO ()
main = do
    input <- getContents
    let ls = words input
        r = read (head ls) :: Int
        c = read (ls !! 1) :: Int
        graellaLines = take r (drop 2 ls)
        recorregut = ls !! (2 + r)
        inici = head [ (i, j) | (i, row) <- zip [0..] graellaLines, (j, val) <- zip [0..] row, val == 'S' ] 
        ans = hits graellaLines recorregut inici Nothing
    print ans
