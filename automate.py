import csv
from eightpuzzle import EightPuzzleState, EightPuzzleSearchProblem

def run_simulation(initial_state, heuristic_function):
    puzzle = EightPuzzleState(initial_state)
    problem = EightPuzzleSearchProblem(puzzle)
    
    # Set the heuristic function dynamically
    problem.heuristic = heuristic_function

    # Run A* search
    path = problem.aStarSearch()

    # Return results
    return {
        'depth': len(path),
        'expanded_nodes': problem.expanded_nodes,
        'fringe_size': problem.fringe_size
    }

def read_scenarios_from_csv(csv_filename):
    scenarios = []

    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            scenarios.append(row)

    return scenarios

def main():
    # Specify the CSV file with scenarios
    scenarios_filename = 'scenarios.csv'

    # Read scenarios from CSV
    scenarios = read_scenarios_from_csv(scenarios_filename)

    # Define heuristic functions
    heuristics = [
        ('h1', EightPuzzleSearchProblem.h1_heuristic),
        ('h2', EightPuzzleSearchProblem.h2_heuristic),
        ('h3', EightPuzzleSearchProblem.h3_heuristic),
        ('h4', EightPuzzleSearchProblem.h4_heuristic),
    ]

    # Run simulations for each scenario and each heuristic
    results = []

    for scenario in scenarios:
        initial_state = list(map(int, scenario['initial_state'].split(',')))
        for heuristic_name, heuristic_function in heuristics:
            result = run_simulation(initial_state, heuristic_function)
            results.append({
                'scenario': scenario['name'],
                'heuristic': heuristic_name,
                'depth': result['depth'],
                'expanded_nodes': result['expanded_nodes'],
                'fringe_size': result['fringe_size'],
            })

    # Tabulate and print the results
    print("{:<15} {:<10} {:<10} {:<15} {:<15}".format(
        'Scenario', 'Heuristic', 'Depth', 'Expanded Nodes', 'Fringe Size'
    ))
    for result in results:
        print("{:<15} {:<10} {:<10} {:<15} {:<15}".format(
            result['scenario'], result['heuristic'], result['depth'],
            result['expanded_nodes'], result['fringe_size']
        ))

    # Calculate averages or any other analysis you want to perform

if __name__ == '__main__':
    main()
