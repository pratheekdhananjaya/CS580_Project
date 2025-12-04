# CS580 Project

This repository contains the code for the CS580 project.

## Contents

- `Q1.py` – Hash join for $q(A,B,C) :- R1(A,B), R2(B,C)$ with a 10×10 synthetic dataset and printed join results.
- `Q2.py` – Simplified Yannakakis algorithm for a line join using a small verification dataset that demonstrates dangling-tuple removal.
- `Q3.py` – Naive sequential line-join implementation for the same line query as Q2, materializing full intermediate results.
- `Q4.py` – Generates a random 3-line dataset (100 tuples per relation) and compares runtime and output equality of the Q2 (Yannakakis) and Q3 (naive) algorithms.
- `Q5.py` – Generates a specific dataset and compares runtime and output equality of the same two algorithms.
- `Q6.py` – SQL generator; creates `problem6_data.sql` that builds MySQL tables R1, R2, R3 with the Problem 5 dataset and a `SELECT` 3-way join query for external timing.
- `Q7.py` – Implementations of GenericJoin, GHW and FHW, load `R1.csv`–`R7.csv`, run all three algorithms, and compare runtimes and result sets.


## Requirements

- Python: 3.8+
- Standard library only (uses `collections`, `random`, `time`, `csv`, `os`, `random`). 
- For Q6 / MySQL experiment:
    - MySQL server and client tools (MySQL Workbench) installed.


## Steps to Run

From this directory:

- **Q1 – Hash join**

```bash
python Q1.py
```

- **Q2 – Yannakakis line join**

```bash
python Q2.py
```

- **Q3 – Naive line join**

```bash
python Q3.py
```

- **Q4 – Random 3-line experiment**

```bash
python Q4.py
```

- **Q5 – Adversarial 3-line experiment**

```bash
python Q5.py
```

- **Q6 – MySQL script generation**

```bash
python Q6.py
```

Creates `problem6_data.sql`. Then, in MySQL:

```sql
SOURCE problem6_data.sql;
```

- **Q7 – GenericJoin / GHW / FHW**

Place `R1.csv`–`R7.csv` in the same directory and run:

```bash
python Q7.py
```