import collections
import random
import time

# Problem 2 implementation
class Problem2Solver:
    def solve(self, relations):
        chain = [list(r) for r in relations]
        numberOfRelations = len(chain)

        for i in range(numberOfRelations - 2, -1, -1):
            rightRelation = chain[i + 1]
            validKeys = set(r[0] for r in rightRelation)

            chain[i] = [r for r in chain[i] if r[1] in validKeys]

        currentResult = chain[0]
        for i in range(1, numberOfRelations):
            nextResult = chain[i]
            idx = collections.defaultdict(list)
            for r in nextResult:
                idx[r[0]].append(r)

            newResult = []
            for tup in currentResult:
                key = tup[-1]
                if key in idx:
                    for match in idx[key]:
                        newResult.append(tup + (match[1],))
            currentResult = newResult

        return currentResult


# Problem 3 implementation
class Problem3Solver:
    def solve(self, relations):
        currentResult = relations[0]

        for i in range(1, len(relations)):
            nextResult = relations[i]

            # Build index
            idx = collections.defaultdict(list)
            for r in nextResult:
                idx[r[0]].append(r)

            newResult = []
            for tup in currentResult:
                key = tup[-1]
                if key in idx:
                    for match in idx[key]:
                        newResult.append(tup + (match[1],))
            currentResult = newResult

        return currentResult


# Problem 5 dataset
class ExperimentRunner:
    def GenerateProblem5Dataset(self):
        print("Generating Problem 5 Dataset:")
        random.seed(42)

        # R1 Generation in 3 parts
        # 1000 tuples ending in 5
        r1Part1 = [(i, 5) for i in range(1, 1001)]
        # 1000 tuples ending in 7
        r1Part2 = [(i, 7) for i in range(1001, 2001)]
        # The "Needle in the Haystack" tuple
        r1Part3 = [(2001, 2002)]

        self.R1 = r1Part1 + r1Part2 + r1Part3
        random.shuffle(self.R1)

        # R2 Generation in 3 parts 
        # 1000 tuples starting with 5 (Matches r1Part1)
        r2Part1 = [(5, i) for i in range(1, 1001)]
        # 1000 tuples starting with 7 (Matches r1Part2)
        r2Part2 = [(7, i) for i in range(1001, 2001)]
        # The "Needle" continuation
        r2Part3 = [(2002, 8)]

        self.R2 = r2Part1 + r2Part2 + r2Part3
        random.shuffle(self.R2)

        # R3 Generation
        r3Random = [(random.randint(2002, 3000), random.randint(1, 3000)) for _ in range(2000)]
        r3Valid = [(8, 30)]

        self.R3 = r3Random + r3Valid
        random.shuffle(self.R3)

        self.dataset = [self.R1, self.R2, self.R3]
        print(f"Dataset Sizes: R1={len(self.R1)}, R2={len(self.R2)}, R3={len(self.R3)}")

    def RunComparison(self):
        problem2Solver = Problem2Solver()
        problem3Solver = Problem3Solver()

        print("\nRunning Problem 2 Implementation (Yannakakis):")
        startTimeProblem2 = time.perf_counter()
        resultProblem2 = problem2Solver.solve(self.dataset)
        endTimeProblem2 = time.perf_counter()
        finalTimeProblem2 = (endTimeProblem2 - startTimeProblem2) * 1000

        print(f"Yannakakis Time (Problem 2): {finalTimeProblem2:.4f} ms")
        print(f"Result Size: {len(resultProblem2)}")

        print("\nRunning Problem 3 Implementation (Naive):")
        startTimeProblem3 = time.perf_counter()
        resultProblem3 = problem3Solver.solve(self.dataset)
        endTimeProblem3 = time.perf_counter()
        finalTimeProblem3 = (endTimeProblem3 - startTimeProblem3) * 1000

        print(f"Naive Time (Problem 3): {finalTimeProblem3:.4f} ms")
        print(f"Result Size: {len(resultProblem3)}")

        print("\nProblem 2 Implementation (Yannakakis) Output: ", resultProblem2)
        print("\nProblem 3 Implementation (Naive) Output: ", resultProblem3)

        if set(resultProblem2) == set(resultProblem3):
            print("\nBoth algorithms returned the same result set.")
        else:
            print("\nResult sets differ.")


if __name__ == "__main__":
    runner = ExperimentRunner()
    runner.GenerateProblem5Dataset()
    runner.RunComparison()