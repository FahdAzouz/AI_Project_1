import csv
from eightpuzzle import EightPuzzleState, EightPuzzleSearchProblem

def read_configurations(file_path):
    """
    Read configurations from the CSV file.
    Each row in the CSV file represents a configuration.
    """
    configurations = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            configurations.append(list(map(int, row)))
    return configurations

def run_scenario(initial_state, heuristic_func):
    """
    Run a scenario for a given initial state and heuristic function.
    Return the path length.
    """
    problem = EightPuzzleSearchProblem(EightPuzzleState([initial_state]))
    path = problem.aStarSearch(heuristic=heuristic_func)
    return len(path)

def main():
    # Read configurations from scenarios.csv
    configurations = read_configurations('scenarios.csv')

    # Define heuristics
    heuristics = [
        ('h1', EightPuzzleSearchProblem.h1_heuristic),
        ('h2', EightPuzzleSearchProblem.h2_heuristic),
        ('h3', EightPuzzleSearchProblem.h3_heuristic),
        ('h4', EightPuzzleSearchProblem.h4_heuristic),
    ]

    # Run scenarios and record average path lengths
    results = []

    for heuristic_name, heuristic_func in heuristics:
        avg_lengths = []
        for config in configurations:
            total_length = 0
            for initial_state in config:
                length = run_scenario(initial_state, heuristic_func)
                total_length += length
            avg_lengths.append(total_length / len(config))

        results.append({
            'heuristic': heuristic_name,
            'avg_lengths': avg_lengths,
        })

    # Print or save the results as needed
    for result in results:
        print(f"Heuristic: {result['heuristic']}")
        print(f"Avg Path Lengths: {result['avg_lengths']}")
        print()

if __name__ == '__main__':
    main()
