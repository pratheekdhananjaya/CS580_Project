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

            # Filter left relation
            chain[i] = [r for r in chain[i] if r[1] in validKeys]

        currentResult = chain[0]
        for i in range(1, numberOfRelations):
            nextRelation = chain[i]
            idx = collections.defaultdict(list)
            for r in nextRelation:
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
            nextRelation = relations[i]

            idx = collections.defaultdict(list)
            for r in nextRelation:
                idx[r[0]].append(r)

            newResult = []
            for tup in currentResult:
                key = tup[-1]
                if key in idx:
                    for match in idx[key]:
                        newResult.append(tup + (match[1],))
            currentResult = newResult

        return currentResult


# Problem 4 dataset
class ExperimentRunner:
    def GenerateRandomDataset(self):
        print("Generating Random Dataset:")
        random.seed(42)

        # R1: 100 tuples (i, x), i=1..100, x in [1, 5000]
        self.R1 = [(i, random.randint(1, 5000)) for i in range(1, 101)]

        # R2: 100 tuples (y, j), j=1..100, y in [1, 5000]
        self.R2 = [(random.randint(1, 5000), j) for j in range(1, 101)]

        # R3: 100 tuples (l, l), l=1..100
        self.R3 = [(l, l) for l in range(1, 101)]

        self.dataset = [self.R1, self.R2, self.R3]
        print(f"Dataset Sizes: R1={len(self.R1)}, R2={len(self.R2)}, R3={len(self.R3)}")

    def RunComparison(self):
        problem2Solver = Problem2Solver()
        problem3Solver = Problem3Solver()

        print("\nProblem 2 Implementation (Yannakakis):")
        startTimeProblem2 = time.perf_counter()
        resultProblem2 = problem2Solver.solve(self.dataset)
        endTimeProblem2 = time.perf_counter()
        finalTimeProblem2 = (endTimeProblem2 - startTimeProblem2) * 1000

        print(f"Yannakakis Time (Problem 2): {finalTimeProblem2:.4f} ms")
        print(f"Result Size: {len(resultProblem2)}")

        print("\nProblem 3 Implementation (Naive):")
        startTimeProblem3 = time.perf_counter()
        resultProblem3 = problem3Solver.solve(self.dataset)
        endTimeProblem3 = time.perf_counter()
        finalTimeProblem3 = (endTimeProblem3 - startTimeProblem3) * 1000

        print(f"Naive Time (Problem 3): {finalTimeProblem3:.4f} ms")
        print(f"Result Size: {len(resultProblem3)}")

        problem2Set = set(resultProblem2)
        problem3Set = set(resultProblem3)

        if problem2Set == problem3Set:
            print("\nBoth algorithms returned the same result set.")
        else:
            print("\nResult sets differ.")


if __name__ == "__main__":
    runner = ExperimentRunner()
    runner.GenerateRandomDataset()
    runner.RunComparison()