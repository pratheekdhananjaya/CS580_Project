import collections
import time
import csv
import os

# GenericJoin Algorithm
class GenericJoinSolver:
    def __init__(self, relations):
        self.relations = relations
        # Indices: table -> col_index -> value -> list_of_tuples
        self.indices = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
        self.BuildIndices()

    def BuildIndices(self):
        # Build hash indices for all columns of all relations to allow O(1) lookups
        for name, rows in self.relations.items():
            for row in rows:
                self.indices[name][0][row[0]].append(row)
                self.indices[name][1][row[1]].append(row)

    def GetCandidates(self, var, assignments):
        candidates = None

        def intersect(newSet):
            nonlocal candidates
            if candidates is None:
                candidates = newSet
            else:
                candidates = candidates & newSet

        if var == 'A1':
            intersect(set(self.indices['R1'][0].keys()))
            intersect(set(self.indices['R3'][0].keys()))
        elif var == 'A2':
            a1 = assignments['A1']
            validR1 = set(r[1] for r in self.indices['R1'][0].get(a1, []))
            intersect(validR1)
            intersect(set(self.indices['R2'][0].keys()))
        elif var == 'A3':
            a1, a2 = assignments['A1'], assignments['A2']
            validR2 = set(r[1] for r in self.indices['R2'][0].get(a2, []))
            validR3 = set(r[1] for r in self.indices['R3'][0].get(a1, []))
            intersect(validR2)
            intersect(validR3)
            intersect(set(self.indices['R4'][0].keys()))
        elif var == 'A4':
            a3 = assignments['A3']
            validR4 = set(r[1] for r in self.indices['R4'][0].get(a3, []))
            intersect(validR4)
            intersect(set(self.indices['R5'][0].keys()))
            intersect(set(self.indices['R7'][0].keys()))
        elif var == 'A5':
            a4 = assignments['A4']
            validR5 = set(r[1] for r in self.indices['R5'][0].get(a4, []))
            intersect(validR5)
            intersect(set(self.indices['R6'][0].keys()))
        elif var == 'A6':
            a4, a5 = assignments['A4'], assignments['A5']
            validR6 = set(r[1] for r in self.indices['R6'][0].get(a5, []))
            validR7 = set(r[1] for r in self.indices['R7'][0].get(a4, []))
            intersect(validR6)
            intersect(validR7)

        return candidates if candidates else set()

    def solve(self):
        results = []
        for a1 in self.GetCandidates('A1', {}):
            c1 = {'A1': a1}
            for a2 in self.GetCandidates('A2', c1):
                c2 = {**c1, 'A2': a2}
                for a3 in self.GetCandidates('A3', c2):
                    c3 = {**c2, 'A3': a3}
                    for a4 in self.GetCandidates('A4', c3):
                        c4 = {**c3, 'A4': a4}
                        for a5 in self.GetCandidates('A5', c4):
                            c5 = {**c4, 'A5': a5}
                            for a6 in self.GetCandidates('A6', c5):
                                results.append((a1, a2, a3, a4, a5, a6))
        return results


# Generalized Hypertree Width algorithm
class GHW:
    def solve(self, relations):
        idxR2 = collections.defaultdict(list)
        for r in relations['R2']: idxR2[r[0]].append(r)
        setR3 = set(relations['R3'])

        bag1 = []
        for r1 in relations['R1']:
            a1, a2 = r1
            if a2 in idxR2:
                for r2 in idxR2[a2]:
                    a3 = r2[1]
                    if (a1, a3) in setR3:
                        bag1.append((a1, a2, a3))

        idxR6 = collections.defaultdict(list)
        for r in relations['R6']: idxR6[r[0]].append(r)
        setR7 = set(relations['R7'])

        bag3 = []
        for r5 in relations['R5']:
            a4, a5 = r5
            if a5 in idxR6:
                for r6 in idxR6[a5]:
                    a6 = r6[1]
                    if (a4, a6) in setR7:
                        bag3.append((a4, a5, a6))

        idxR4 = collections.defaultdict(list)
        for r in relations['R4']: idxR4[r[0]].append(r)

        idxBag3 = collections.defaultdict(list)
        for r in bag3: idxBag3[r[0]].append(r)

        results = []
        for b1 in bag1:
            a3 = b1[2]
            if a3 in idxR4:
                for r4 in idxR4[a3]:
                    a4 = r4[1]
                    if a4 in idxBag3:
                        for b3 in idxBag3[a4]:
                            results.append(b1 + (a4,) + b3[1:])
        return results


# Fractional Hypertree Width algorithm
class FHW:
    def solve(self, relations):
        def Triangle1():
            idxR1 = collections.defaultdict(list)
            for r in relations['R1']: idxR1[r[0]].append(r)
            idxR2 = collections.defaultdict(list)
            for r in relations['R2']: idxR2[r[0]].append(r)
            idxR3A3 = collections.defaultdict(set)
            for r in relations['R3']: idxR3A3[r[1]].add(r[0])
            idxR3A1 = collections.defaultdict(set)
            for r in relations['R3']: idxR3A1[r[0]].add(r[1])

            res = []
            keysA1 = set(idxR1.keys()) & set(idxR3A1.keys())
            for a1 in keysA1:
                validA2S = [r[1] for r in idxR1[a1]]
                for a2 in validA2S:
                    if a2 in idxR2:
                        validA3S = [r[1] for r in idxR2[a2]]
                        for a3 in validA3S:
                            if a1 in idxR3A3[a3]:
                                res.append((a1, a2, a3))
            return res

        def Triangle2():
            idxR5 = collections.defaultdict(set)
            for r in relations['R5']: idxR5[r[0]].add(r[1])
            idxR6 = collections.defaultdict(set)
            for r in relations['R6']: idxR6[r[1]].add(r[0])

            res = []
            for r7 in relations['R7']:
                a4, a6 = r7
                validA5S = idxR5[a4] & idxR6[a6]
                for a5 in validA5S:
                    res.append((a4, a5, a6))
            return res

        bag1Results = Triangle1()
        bag3Results = Triangle2()

        idxR4 = collections.defaultdict(list)
        for r in relations['R4']: idxR4[r[0]].append(r)
        idxBag3 = collections.defaultdict(list)
        for r in bag3Results: idxBag3[r[0]].append(r)

        results = []
        for b1 in bag1Results:
            a3 = b1[2]
            if a3 in idxR4:
                for r4 in idxR4[a3]:
                    a4 = r4[1]
                    if a4 in idxBag3:
                        for b3 in idxBag3[a4]:
                            results.append(b1 + (a4,) + b3[1:])
        return results

# Load data
def LoadCSVData():
    data = {}
    print(f"Loading data from current directory:")
    try:
        for i in range(1, 8):
            key = f"R{i}"
            filename = f"{key}.csv"

            with open(filename, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if rows and not rows[0][0].isdigit():
                    rows = rows[1:]

                data[key] = [tuple(map(int, r)) for r in rows]
            print(f"Loaded {key}: {len(data[key])} tuples")
    except FileNotFoundError:
        print("ERROR: Could not find R1-R7 CSV files.")
        return None
    return data


if __name__ == "__main__":
    dataset = LoadCSVData()

    if dataset:
        print("\nProblem 7 Comparison")

        # 1. Generic Join
        gj = GenericJoinSolver(dataset)
        timeStart = time.perf_counter()
        resultGJ = gj.solve()
        timeEnd = time.perf_counter()
        print(f"GenericJoin Time: {(timeEnd - timeStart):.4f} sec. Result Size: {len(resultGJ)}")

        # 2. GHW
        ghw = GHW()
        timeStart = time.perf_counter()
        resultGHW = ghw.solve(dataset)
        timeEnd = time.perf_counter()
        print(f"GHW Time: {(timeEnd - timeStart):.4f} sec. Result Size: {len(resultGHW)}")

        # 3. FHW
        fhw = FHW()
        timeStart = time.perf_counter()
        resultFHW = fhw.solve(dataset)
        timeEnd = time.perf_counter()
        print(f"FHW Time: {(timeEnd - timeStart):.4f} sec. Result Size: {len(resultFHW)}")

        # Verifying through length/sizes
        match = (len(resultGJ) == len(resultGHW) == len(resultFHW))
        print(f"\nVerification: Do the sizes match? {match}")

        # Verifying through results
        GJandGHW = (set(resultGJ) == set(resultGHW))
        GJandFHW = (set(resultGJ) == set(resultFHW))
        GHWandFHW = (set(resultGHW) == set(resultFHW))
        match = GJandGHW and GJandFHW and GHWandFHW

        print(f"\nVerification: Do results match? {match}")