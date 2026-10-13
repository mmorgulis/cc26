# Python Modern Cookbook (3.8+)

## 1. Cicli e Iterazione Idiomatica

### Iterazione Diretta (For-Each)
Evita di accedere agli elementi tramite indici se non è necessario.

```python
colors = ["rosso", "verde", "blu"]

for color in colors:
    print(color)
```

---

### Iterazione Inversa
Usa `reversed()` per scorrere una sequenza al contrario senza modificarla in loco.

```python
colors = ["rosso", "verde", "blu"]

for color in reversed(colors):
    print(color)
```

---

### Indice ed Elemento (`enumerate`)
Usa `enumerate()` per tracciare la posizione senza gestire manualmente un contatore.

```python
colors = ["rosso", "verde", "blu"]

for i, color in enumerate(colors, start=1):
    print(f"{i}: {color}")
```

---

### Iterare su Più Liste in Parallelo (`zip`)
In Python 3 `zip()` genera un iteratore pigro (lazy) a memoria ottimizzata. In Python 3.10+ puoi usare `strict=True` per verificare che le liste abbiano la stessa lunghezza.

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

for name, age in zip(names, ages, strict=True):
    print(f"{name} ha {age} anni")
```

---

### Ordinamento Personalizzato (`sorted`)
Usa il parametro `key` per specificare la logica di ordinamento.

```python
colors = ["rosso", "blu", "giallo", "verde"]

# Ordina per lunghezza della stringa
sorted_colors = sorted(colors, key=len)
print(sorted_colors)  # ['blu', 'rosso', 'verde', 'giallo']
```

---

### Lettura con Sentinella e Walrus Operator (`:=`)
Per cicli `while` che leggono dati fino a una condizione di stop, il **Walrus Operator** (Python 3.8+) rende il codice compatto e leggibile.

```python
from functools import partial

# Metodo con iter() e sentinella
for block in iter(partial(file_obj.read, 64), ''):
    process(block)

# Metodo moderno con Walrus Operator
while (block := file_obj.read(64)) != '':
    process(block)
```

---

### Clausola `else` nei Cicli
Il blocco `else` viene eseguito solo se il ciclo termina **senza** incontrare un `break`.

```python
def find_item(items, target):
    for item in items:
        if item == target:
            print("Trovato!")
            break
    else:
        # Eseguito solo se il ciclo si completa interamente
        print("Elemento non presente nel ciclo.")
```

---

## 2. Dizionari e Collezioni Avanzate

### Iterazione Efficiente su Chiavi e Valori
`dict.items()` restituisce una vista dinamica efficiente senza duplicare la memoria.

```python
d = {"matteo": "blu", "rachel": "rosso"}

for key, value in d.items():
    print(f"{key} predilige il {value}")
```

---

### Modifica di un Dizionario durante l'Iterazione
Non modificare mai un dizionario mentre ci iteri direttamente sopra. Usa `list(d.keys())` oppure una *Dictionary Comprehension*.

```python
d = {"a": 1, "b": 2, "c": 3}

# Modifica in loco sicura tramite lista di chiavi
for k in list(d.keys()):
    if d[k] < 2:
        del d[k]

# Oppure tramite Dictionary Comprehension (più pythonico)
d = {k: v for k, v in d.items() if v >= 2}
```

---

### Creazione Rapida da Due Liste
Combina `dict()` e `zip()` per creare dizionari al volo.

```python
keys = ["nome", "ruolo", "livello"]
values = ["Mario", "Dev", 5]

user = dict(zip(keys, values))
# {'nome': 'Mario', 'ruolo': 'Dev', 'livello': 5}
```

---

### Conteggio Intelligente (`Counter` vs `defaultdict`)
Per contare le frequenze, `collections.Counter` è la soluzione standard e più veloce.

```python
from collections import Counter, defaultdict

colors = ["rosso", "blu", "rosso", "verde", "blu", "rosso"]

# Metodo 1: Counter (Consigliato)
counts = Counter(colors)
print(counts["rosso"])  # 3

# Metodo 2: defaultdict
d = defaultdict(int)
for color in colors:
    d[color] += 1
```

---

### Raggruppamento Dati (`defaultdict`)
Usa `defaultdict(list)` per raggruppare elementi senza dover gestire il controllo di esistenza delle chiavi.

```python
from collections import defaultdict

names = ["Alice", "Bob", "Amanda", "Bruno", "Carlo"]
grouped = defaultdict(list)

for name in names:
    first_letter = name[0]
    grouped[first_letter].append(name)

# {'A': ['Alice', 'Amanda'], 'B': ['Bob', 'Bruno'], 'C': ['Carlo']}
```

---

### Unione e Collegamento di Dizionari
In Python 3.9+ puoi unire i dizionari con gli operatori `|` e `|=`. Usa `ChainMap` se non vuoi allocare nuova memoria.

```python
from collections import ChainMap

d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}

# Unione diretta (Python 3.9+) -> crea un nuovo dizionario
merged = d1 | d2  # {'a': 1, 'b': 99, 'c': 3}

# Vista combinata senza copiare i dati
chain = ChainMap(d1, d2)
print(chain["b"])  # 2 (prende il primo incontrato)
```

---

## 3. Strutture Dati e Pattern Moderni

### Data Classes e Type Hints
Invece di `namedtuple`, in Python moderno si usano spesso le `@dataclass` (disponibili da Python 3.7+).

```python
from dataclasses import dataclass

@dataclass
class Persona:
    nome: str
    eta: int
    citta: str = "Roma"

p = Persona(nome="Mario", eta=30)
print(f"{p.nome} vive a {p.citta}")
```

---

### Unpacking Avanzato
Python permette di estrarre elementi in modo elegante sia da tuple che da liste.

```python
# Assegnamento atomico (scambio variabili)
a, b = 1, 2
a, b = b, a

# Unpacking di sequenze
persona = ("Mario", "Rossi", 30, "Sviluppatore")
nome, cognome, *dettagli = persona

# 'dettagli' conterrà [30, 'Sviluppatore']
```

---

### Formattazione con f-string e Concatenazione
Usa le f-string per comporre testo e variabili, e `.join()` solo per collezioni di stringhe.

```python
# f-string (Python 3.6+)
nome = "Luca"
punti = 42
print(f"L'utente {nome} ha ottenuto {punti} punti.")

# Concatenazione efficace di collezioni
parole = ["Python", "è", "fantastico"]
frase = " ".join(parole)
```

---

### Caching delle Funzioni con `@cache`
Da Python 3.9, `@functools.cache` permette di memorizzare i risultati di funzioni senza configurazioni complesse.

```python
from functools import cache

@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# I calcoli già effettuati saranno istantanei
print(fibonacci(100))
```
