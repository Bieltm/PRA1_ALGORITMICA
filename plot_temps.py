import re
import matplotlib.pyplot as plt

def parse_file(filename):
    data = {}
    current_step = None
    # /usr/bin/time -p outputs: real 0.05
    time_re = re.compile(r'real\s+([\d.]+)')
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('STEP'):
                    current_step = int(line.split()[1])
                    if current_step not in data:
                        data[current_step] = []
                else:
                    m = time_re.search(line)
                    if m and current_step is not None:
                        data[current_step].append(float(m.group(1)))
    except FileNotFoundError:
        print(f"Fitxer {filename} no trobat.")
        return [], []
        
    steps = sorted(data.keys())
    # Calcular la mitjana de temps per a cada quantitat de passos
    avgs = [sum(data[s])/len(data[s]) if data[s] else 0 for s in steps]
    return steps, avgs

hs_steps, hs_avgs = parse_file('temps_plot_hs.txt')
py_steps, py_avgs = parse_file('temps_plot_py.txt')

if hs_steps:
    plt.figure()
    plt.plot(hs_steps, hs_avgs, marker='o', color='blue')
    plt.title("Temps d'execució - Haskell")
    plt.xlabel('Nombre de passos del robot')
    plt.ylabel('Temps mitjà de resolució (s)')
    plt.xticks(hs_steps)
    plt.grid(True)
    plt.savefig('plot_haskell.png')
    print("Gràfica desada a plot_haskell.png")

if py_steps:
    plt.figure()
    plt.plot(py_steps, py_avgs, marker='o', color='red')
    plt.title("Temps d'execució - Python")
    plt.xlabel('Nombre de passos del robot')
    plt.ylabel('Temps mitjà de resolució (s)')
    plt.xticks(py_steps)
    plt.grid(True)
    plt.savefig('plot_python.png')
    print("Gràfica desada a plot_python.png")
