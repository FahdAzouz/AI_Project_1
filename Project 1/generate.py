import csv
from eightpuzzle import createRandomEightPuzzle

def generate_configurations(num_configurations, moves_per_configuration):
    """
    Generate random configurations for the 8-puzzle.
    Each configuration is represented as a list of integers.
    """
    configurations = []
    for _ in range(num_configurations):
        puzzle = createRandomEightPuzzle(moves=moves_per_configuration)
        configuration = [cell for row in puzzle.cells for cell in row]

        # Ensure that the configuration has exactly 9 numbers
        if len(configuration) != 9:
            raise ValueError("Invalid configuration: not enough numbers.")

        configurations.append(configuration)

    return configurations

def write_to_csv(file_path, configurations):
    """
    Write configurations to a CSV file.
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for config in configurations:
            writer.writerow(config)

if __name__ == '__main__':
    num_configurations = 100
    moves_per_configuration = 25
    output_file_path = 'scenarios.csv'

    configurations = generate_configurations(num_configurations, moves_per_configuration)
    write_to_csv(output_file_path, configurations)
    print(f'{num_configurations} configurations written to {output_file_path}')
