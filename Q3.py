import collections


class NaiveLineJoiner:
    def __init__(self):
        self.relations = []

    def loadData(self):
        R1 = [(1, 2), (10, 20), (99, 100)]
        R2 = [(2, 3), (20, 30), (55, 66)]
        R3 = [(3, 4), (7, 8)]

        self.relations = [R1, R2, R3]

        print("Input Data:")
        for i, r in enumerate(self.relations):
            print(f"R{i + 1}: {r}")

    def executeSequentialJoin(self):
        # Starting with R1 as the base result
        currentResult = self.relations[0]

        # Iterating through the rest of the relations
        for i in range(1, len(self.relations)):
            nextRelation = self.relations[i]
            print(f"   Step {i}: Joining current result (size {len(currentResult)}) with R{i + 1} (size {len(nextRelation)})...")

            hashIdx = collections.defaultdict(list)
            for row in nextRelation:
                key = row[0]
                hashIdx[key].append(row)

            newResult = []
            for tup in currentResult:
                key = tup[-1]

                if key in hashIdx:
                    matches = hashIdx[key]
                    for match in matches:
                        extendedTuple = tup + (match[1],)
                        newResult.append(extendedTuple)

            currentResult = newResult
            print(f"Intermediate Result Size: {len(currentResult)}")
            # For demonstration, let's print the intermediate tuples
            print(f"Data: {currentResult}")

        return currentResult

if __name__ == "__main__":
    joiner = NaiveLineJoiner()
    joiner.loadData()
    finalResult = joiner.executeSequentialJoin()

    print("\nFinal Result:")
    print(finalResult)