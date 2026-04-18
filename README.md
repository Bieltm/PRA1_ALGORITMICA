Funcionament General de l'Algorisme
L'objectiu principal és calcular el nombre mínim de canvis (impactes de rajos còsmics) que ha patit la permutació de prioritats del robot per fer que el seu recorregut sigui coherent amb el terreny.
Prioritat de Direccions: El robot disposa de 4 direccions (N, S, E, O), fet que genera 24 permutacions possibles d'ordre de prioritat.
Lògica de Filtratge: Per a cada moviment realitzat, l'algorisme identifica quines direccions eren "practicables" (sense obstacles) des de la posició actual. 
Una permutació es manté com a vàlida només si el moviment realitzat hi apareix amb més prioritat que qualsevol altra opció practicable en aquell moment.
Detecció del "Raig": Quan la llista de permutacions candidates es queda buida (cap de les 24 combinacions pot explicar el moviment actual), es confirma que un raig còsmic ha alterat la memòria del robot.Processament en cas d'Impacte
Quan es detecta un raig, l'algorisme actua de la següent manera:
Incrementa el comptador de rajos còsmics.Reinicia la llista de permutacions, tornant a considerar les 24 inicials però aplicant immediatament la restricció del moviment que s'acaba de realitzar per filtrar les noves candidates.Implementació TècnicaL'algorisme s'ha estructurat en dues variants:Iterativa (Python): Utilitza un bucle for per recórrer la seqüència de passos, actualitzant la posició i el conjunt de permutacions vàlides en cada iteració.
Recursiva (Haskell): Processa la llista de moviments mitjançant recursivitat o funcions d'ordre superior com foldl', mantenint l'estat del cost mínim per a cada permutació al llarg de tot el camí.# PRA1_ALGORITMICA
