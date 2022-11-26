import sys
import main as mn


def main(**kwargs):

    """
    n = kwargs.get('n')
    if n == None:
        n = 1
    n = int(n)

    fname = kwargs.get('fname')
    if fname == None:
        fname = 'output'
    """
    evo_rates = [0.001, 0.002, 0.004, 0.006, 0.008, 0.01]
    n = 5

    total_runs = len(evo_rates) * n

    fname = "evo_test_"

    print()
    print("LAUNCHER")
    print("Running", n, "iterations, saving to", fname)
    print()

    totalCount = 0
    
    for rate in evo_rates:

        for i in range(n):
            filename = fname + '_' + str(rate) + '_' + str(i)

            window_title = "Run " + str(totalCount) + " of " + str(total_runs) + " - evo_rate: " + str(rate)

            result = mn.main(
                record=True, fname=filename, evorate=rate, window_title=window_title
            )

            totalCount += 1

    return 0


if __name__ == "__main__":
    main(
        **dict(
            arg.split('=') for arg in sys.argv[1:]
        )
    )