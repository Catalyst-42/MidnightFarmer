from random import randint

runs = []

for _ in range(10_000):
    run = 1
    while randint(1, 3_000) != 1:
        run += 1

    runs.append(run)

print(runs, sum(runs) / len(runs))
