import collections

class HashJoiner:
    def __init__(self):
        self.R1 = []
        self.R2 = []

    def generateDataset(self):
        self.R1 = [
            (1, 10), (2, 20), (3, 30), (4, 40), (5, 50),
            (6, 60), (7, 20), (8, 30), (9, 10), (10, 99)
        ]
        self.R2 = [
            (10, 100), (20, 200), (30, 300), (40, 400), (10, 101),
            (20, 201), (55, 500), (66, 600), (77, 700), (88, 800)
        ]

        print("Input Data:")
        print(f"R1 (Size {len(self.R1)}): {self.R1}")
        print(f"R2 (Size {len(self.R2)}): {self.R2}")
        print("\n")

    def executeJoin(self):
        print("Step 1: Building Hash Map on R2")

        hashmap = collections.defaultdict(list)

        for row in self.R2:
            key = row[0]
            hashmap[key].append(row)

        print(f"Hash Map Keys Created: {list(hashmap.keys())}")

        print("\nStep 2: Probing Hash Map with R1")
        results = []

        for row in self.R1:
            key = row[1]

            if key in hashmap:
                matches = hashmap[key]

                for R2match in matches:
                    joinedTuple = (row[0], row[1], R2match[1])
                    results.append(joinedTuple)

        return results

if __name__ == "__main__":
    joiner = HashJoiner()
    joiner.generateDataset()
    joinedOutput = joiner.executeJoin()

    print("\nFinal Join Results (A, B, C):")
    print(f"Total rows: {len(joinedOutput)}")
    for row in joinedOutput:
        print(row)