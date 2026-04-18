import sys
import time
from itertools import permutations

# Augmentem el límit per seguretat (encara que fem servir la iterativa)
sys.setrecursionlimit(30000)

# --- DECORADOR ---
def mesurar_temps(funcio):
    def embolcall(*args, **kwargs):
        inici = time.time()
        resultat = funcio(*args, **kwargs)
        final = time.time()
        # El temps es pot imprimir o guardar si es vol
        return resultat
    return embolcall

# --- FUNCIONS AUXILIARS ---

def llegir_entrada():
    """Llegeix les dades d'arxiu o stdin segons l'especificació[cite: 60]."""
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            linies = [l.strip() for l in f.readlines() if l.strip()]
    else:
        linies = [l.strip() for l in sys.stdin.readlines() if l.strip()]
    
    if not linies: return None

    try:
        # files i columnes acotades a 200 
        r, c = map(int, linies[0].split())
        graella = linies[1:r+1]
        passos = linies[r+1] if len(linies) > r+1 else ""
        
        # Llista per comprensió per trobar la 'S' inicial [cite: 33, 53]
        pos_S = next((i, j) for i, fila in enumerate(graella) 
                     for j, char in enumerate(fila) if char == 'S')
        return graella, passos, pos_S
    except (ValueError, IndexError, StopIteration):
        return None

def obtenir_direccions_possibles(graella, pos):
    """Generador de direccions practicables[cite: 20, 53]."""
    movs = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
    r_max, c_max = len(graella), len(graella[0])
    
    for dir_nom, (dr, dc) in movs.items():
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < r_max and 0 <= nc < c_max and graella[nr][nc] != '#':
            yield dir_nom

def filtrar_per_prioritat(permutacions, mov_real, practicables):
    """Filtra permutacions on mov_real és la primera opció practicable[cite: 10, 20]."""
    ops = set(practicables)
    def es_valida(p):
        for d in p:
            if d in ops: return d == mov_real
        return False
    return [p for p in permutacions if es_valida(p)]

# --- ALGORISME ITERATIU ---

@mesurar_temps # Ús del decorador obligatori [cite: 53]
def calcular_raigs_iteratiu(graella, passos, pos_inicial):
    comptador_raigs = 0
    pos_actual = pos_inicial
    totes_les_perms = list(permutations(['N', 'S', 'E', 'O']))
    candidates = totes_les_perms
    
    dirs = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}

    for mov in passos:
        # Obtenim practicables amb el generador [cite: 53]
        practicables = list(obtenir_direccions_possibles(graella, pos_actual))
        
        noves = filtrar_per_prioritat(candidates, mov, practicables)
        
        if not noves:
            comptador_raigs += 1 # Impacte de raig còsmic detectat [cite: 13, 27]
            candidates = filtrar_per_prioritat(totes_les_perms, mov, practicables)
        else:
            candidates = noves
        
        # Actualització de posició
        dr, dc = dirs[mov]
        pos_actual = (pos_actual[0] + dr, pos_actual[1] + dc)
        
    return comptador_raigs

if __name__ == "__main__":
    dades = llegir_entrada()
    if dades:
        res = calcular_raigs_iteratiu(dades[0], dades[1], dades[2])
        if len(sys.argv) > 2:
            with open(sys.argv[2], 'w') as f: f.write(str(res) + '\n')
        else:
            print(res)