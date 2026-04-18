# https://gemini.google.com/app/c8f7c53df3e0c961
import random
import argparse
import sys

def generar_instancia(id_fitxer, num_files, num_columnes, num_passos, target_canvis):
    # Comprovació de seguretat inicial
    if target_canvis >= num_passos:
        print(f"❌ Error a la instància {id_fitxer}: El nombre de canvis ({target_canvis}) ha de ser estrictament inferior al nombre de passos ({num_passos}).")
        return False

    # Assegurem que els límits estan dins de la cota de l'enunciat (1 a 200)
    num_files = max(5, min(num_files, 200))
    num_columnes = max(5, min(num_columnes, 200))
    
    direccions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
    tecles_dir = list(direccions.keys())
    
    intent = 0
    path_valid = False
    
    # Intentem generar un camí que no xoqui amb les vores
    while intent < 1000 and not path_valid:
        intent += 1
        r, c = num_files // 2, num_columnes // 2
        path = ""
        caselles_visitades = set([(r, c)])
        
        # Triem exactament en quins passos forçarem un canvi de direcció
        # Hi ha (num_passos - 1) moments possibles per canviar.
        punts_canvi = set(random.sample(range(1, num_passos), target_canvis))
        
        dir_actual = random.choice(tecles_dir)
        path_valid = True
        
        for pas in range(num_passos):
            # Si estem en un punt de canvi, girem cap a una nova direcció
            if pas in punts_canvi:
                possibles_noves = [d for d in tecles_dir if d != dir_actual]
                dir_actual = random.choice(possibles_noves)
                
            path += dir_actual
            dr, dc = direccions[dir_actual]
            r, c = r + dr, c + dc
            
            # Verifiquem que no ens apropem a les vores (marge d'1 casella)
            if not (1 <= r < num_files - 1 and 1 <= c < num_columnes - 1):
                path_valid = False
                break # Si xoquem, descartem aquest camí i tornem a començar
                
            caselles_visitades.add((r, c))
            # Marquem els veïns per no posar-hi roques després
            for v_dr, v_dc in direccions.values():
                caselles_visitades.add((r + v_dr, c + v_dc))
                
    if not path_valid:
        print(f"⚠️ Avís: No s'ha pogut generar un camí vàlid per la instància {id_fitxer}.")
        print("  La graella és massa petita per la quantitat de passos. Prova amb menys passos o una graella més gran.")
        return False

    # Inicialitzem la graella i marquem l'inici
    graella = [['.' for _ in range(num_columnes)] for _ in range(num_files)]
    graella[num_files // 2][num_columnes // 2] = 'S'

    # Afegim roques ('#') només en llocs segurs on no interfereixin amb el camí
    num_roques = (num_files * num_columnes) // 10
    roques_posades = 0
    intents_roques = 0
    while roques_posades < num_roques and intents_roques < 1000:
        rr = random.randint(0, num_files - 1)
        rc = random.randint(0, num_columnes - 1)
        if (rr, rc) not in caselles_visitades and graella[rr][rc] == '.':
            graella[rr][rc] = '#'
            roques_posades += 1
        intents_roques += 1

    # Escrivim l'arxiu d'entrada
    nom_entrada = f"input{id_fitxer}.txt"
    with open(nom_entrada, 'w') as f:
        f.write(f"{num_files} {num_columnes}\n")
        for fila in graella:
            f.write("".join(fila) + "\n")
        f.write(path + "\n")
        
    # Escrivim l'arxiu de sortida amb la solució precalculada
    nom_sortida = f"output{id_fitxer}.txt"
    with open(nom_sortida, 'w') as f:
        f.write(f"{target_canvis}\n") # La solució és exactament els canvis que hem demanat
        
    print(f"✅ Instància {id_fitxer} generada: {num_files}x{num_columnes} | Passos: {num_passos} | Canvis: {target_canvis}")
    return True

if __name__ == "__main__":
    # Configurem el parser d'arguments
    parser = argparse.ArgumentParser(description="Generador d'instàncies per al problema ROC-I.")
    parser.add_argument("files", type=int, help="Nombre de files de la graella")
    parser.add_argument("columnes", type=int, help="Nombre de columnes de la graella")
    parser.add_argument("passos", type=int, help="Nombre total de passos del robot")
    parser.add_argument("canvis", type=int, help="Nombre de canvis de direcció (solució)")
    parser.add_argument("instancies", type=int, help="Nombre d'instàncies a generar")

    # Llegim els arguments introduïts pel terminal
    args = parser.parse_args()

    print(f"Generant {args.instancies} instàncies de {args.files}x{args.columnes} (Passos: {args.passos}, Canvis: {args.canvis})...\n")
    print("-" * 60)

    for i in range(1, args.instancies + 1):
        generar_instancia(
            id_fitxer=i, 
            num_files=args.files, 
            num_columnes=args.columnes, 
            num_passos=args.passos,
            target_canvis=args.canvis
        )
        
    print("-" * 60)