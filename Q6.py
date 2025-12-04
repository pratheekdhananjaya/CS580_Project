import random


def GenerateSQLFile():
    print("Generating problem6_data.sql...")

    with open("problem6_data.sql", "w") as f:
        f.write("CREATE DATABASE IF NOT EXISTS cs580_project;\n")
        f.write("USE cs580_project;\n\n")

        f.write("DROP TABLE IF EXISTS R1;\n")
        f.write("DROP TABLE IF EXISTS R2;\n")
        f.write("DROP TABLE IF EXISTS R3;\n\n")

        f.write("CREATE TABLE R1 (A int, B int);\n")
        f.write("CREATE TABLE R2 (B int, C int);\n")
        f.write("CREATE TABLE R3 (C int, D int);\n\n")

        r1Data = []
        # 1000 tuples (i, 5)
        for i in range(1, 1001): r1Data.append(f"({i}, 5)")
        # 1000 tuples (i, 7)
        for i in range(1001, 2001): r1Data.append(f"({i}, 7)")
        r1Data.append("(2001, 2002)")

        r2Data = []
        # 1000 tuples (5, i)
        for i in range(1, 1001): r2Data.append(f"(5, {i})")
        # 1000 tuples (7, i)
        for i in range(1001, 2001): r2Data.append(f"(7, {i})")
        r2Data.append("(2002, 8)")

        r3Data = []
        random.seed(42)
        for _ in range(2000):
            x = random.randint(2002, 3000)
            y = random.randint(1, 3000)
            r3Data.append(f"({x}, {y})")
        r3Data.append("(8, 30)")

        def InsertStatements(tableName, data):
            batchSize = 1000
            for i in range(0, len(data), batchSize):
                batch = data[i:i + batchSize]
                f.write(f"INSERT INTO {tableName} VALUES {','.join(batch)};\n")

        InsertStatements("R1", r1Data)
        InsertStatements("R2", r2Data)
        InsertStatements("R3", r3Data)

        # Query
        f.write("SELECT SQL_NO_CACHE * \nFROM R1 \nJOIN R2 ON R1.B = R2.B \nJOIN R3 ON R2.C = R3.C;\n")

    print("'problem6_data.sql' created.")


if __name__ == "__main__":
    GenerateSQLFile()