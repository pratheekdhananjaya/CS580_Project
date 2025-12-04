import collections


class YannakakisLineSolver:
    def __init__(self):
        self.chain = []

    def loadVerificationData(self):
        R1 = [(1, 2), (10, 20), (99, 100)]
        # (1, 2): Leads to a full result.
        # (10, 20): Matches R2(20, 30), but R2(20, 30) leads nowhere. (Dangling)
        # (99, 100): No match in R2 at all. (Dangling)

        R2 = [(2, 3), (20, 30), (55, 66)]
        # (2, 3): Matches R1(1,2) and R3(3,4).
        # (20, 30): Matches R1, but has NO match in R3.
        # (55, 66): No match in R1 or R3.

        R3 = [(3, 4), (7, 8)]
        # (3, 4): Completes the chain.
        # (7, 8): Individual.

        self.chain = [R1, R2, R3]

        print("Initial Database:")
        for i, rel in enumerate(self.chain):
            print(f"R{i + 1} (Size {len(rel)}): {rel}")

    def execute(self):
        numRelations = len(self.chain)

        # Iterate from the second-to-last relation down to the first.
        for i in range(numRelations - 2, -1, -1):
            leftRelation = self.chain[i]
            rightRelation = self.chain[i + 1]

            validKeys = set(row[0] for row in rightRelation)

            filtered = []
            for row in leftRelation:
                joinKey = row[1]
                if joinKey in validKeys:
                    filtered.append(row)

            # Update the chain with the reduced relation
            self.chain[i] = filtered

            removedCount = len(leftRelation) - len(filtered)
            print(f"[Reducing R{i + 1}] Kept: {len(filtered)}, Removed: {removedCount} dangling tuples.")

        print("\nRelations After Processing")
        for i, rel in enumerate(self.chain):
            print(f"R{i + 1}: {rel}")

        # Considering the first reduced relation
        currentResults = self.chain[0]

        for i in range(1, numRelations):
            nextRelation = self.chain[i]
            print(f"Joining with R{i + 1}...")
            # Index the next relation for O(1) access
            idxNext = collections.defaultdict(list)
            for row in nextRelation:
                idxNext[row[0]].append(row)

            newResults = []
            for tup in currentResults:
                # The join key is the last element of the current tuple
                key = tup[-1]

                if key in idxNext:
                    matches = idxNext[key]
                    for match in matches:
                        extended = tup + (match[1],)
                        newResults.append(extended)

            currentResults = newResults

        return currentResults

if __name__ == "__main__":
    solver = YannakakisLineSolver()
    solver.loadVerificationData()
    final_output = solver.execute()

    print("\n>>> Final Result (A1...Ak):")
    print(final_output)