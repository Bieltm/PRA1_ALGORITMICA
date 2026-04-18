
TARGET = roc

.PHONY: all test test-hs test-py plot clean

all: $(TARGET)

$(TARGET): roc.hs
	ghc -Wall -O2 -o $(TARGET) $<

test: test-hs test-py

test-hs: $(TARGET)
	@echo "--- Generant 10 instàncies de prova (15x15 amb 8 canvis) ---"
	python3 generador.py 15 15 20 10 10
	@echo "\n--- Executant tests ---"
	@for i in $$(seq 1 10); do \
		echo "Provant instància $$i..."; \
		./$(TARGET) < input$$i.txt > resultat$$i.txt; \
		if diff -q output$$i.txt resultat$$i.txt > /dev/null; then \
			echo "  -> Test $$i: OK"; \
		else \
			echo "  -> Test $$i: ERROR (El resultat no coincideix)"; \
		fi; \
	done

test-py: 
	@echo "--- Generant 10 instàncies de prova (15x15 amb 8 canvis) ---"
	python3 generador.py 10 10 10 5 10
	@echo "\n--- Executant tests ---"
	@for i in $$(seq 1 10); do \
		echo "Provant instància $$i..."; \
		python3 roc.py input$$i.txt resultat$$i.txt; \
		if diff -q output$$i.txt resultat$$i.txt > /dev/null; then \
			echo "  -> Test $$i: OK"; \
		else \
			echo "  -> Test $$i: ERROR (El resultat no coincideix)"; \
		fi; \
	done

clean:
	rm -f $(TARGET) *.o *.hi input*.txt output*.txt resultat*.txt temps_*.txt plot_*.png

plot: $(TARGET)
	@echo "--- Generant dades per al plot de Haskell (fins a 5.000 passos) ---"
	@rm -f temps_plot_hs.txt
	@for pas in $$(seq 1000 1000 5000); do \
		echo "Haskell: 10 instàncies amb $$pas passos..."; \
		echo "STEP $$pas" >> temps_plot_hs.txt; \
		python3 generador.py 200 200 $$pas $$((pas / 10)) 10 > /dev/null; \
		for i in $$(seq 1 10); do \
			(/usr/bin/time -p ./$(TARGET) < input$$i.txt > resultat$$i.txt) 2>> temps_plot_hs.txt; \
		done; \
	done
	@echo "--- Generant dades per al plot de Python (fins a 5.000 passos) ---"
	@rm -f temps_plot_py.txt
	@for pas in $$(seq 1000 1000 5000); do \
		echo "Python: 10 instàncies amb $$pas passos..."; \
		echo "STEP $$pas" >> temps_plot_py.txt; \
		python3 generador.py 200 200 $$pas $$((pas / 10)) 10 > /dev/null; \
		for i in $$(seq 1 10); do \
			(/usr/bin/time -p python3 roc.py input$$i.txt resultat$$i.txt) 2>> temps_plot_py.txt; \
		done; \
	done
	@echo "--- Generant gràfiques ---"
	python3 plot_temps.py
zip:
	zip scripts-roc.zip Makefile generador.py plot_temps.py README.md

