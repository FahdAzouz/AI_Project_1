import csv
from eightpuzzle import createRandomEightPuzzle

def generate_scenarios(num_scenarios, csv_filename):
    scenarios = []

    for i in range(num_scenarios):
        # Generate a random 8-puzzle state
        puzzle = createRandomEightPuzzle()
        initial_state = [cell for row in puzzle.cells for cell in row]

        # Create a scenario name (you can customize this)
        scenario_name = f'Scenario_{i + 1}'

        scenarios.append({
            'name': scenario_name,
            'initial_state': ','.join(map(str, initial_state)),
        })

    # Save scenarios to CSV
    fieldnames = ['name', 'initial_state']
    with open(csv_filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scenarios)

    print(f'{num_scenarios} scenarios generated and saved to {csv_filename}.')

if __name__ == '__main__':
    # Specify the number of scenarios to generate
    num_scenarios = 10

    # Specify the CSV file to save scenarios
    csv_filename = 'scenarios.csv'

    # Generate scenarios and save them to CSV
    generate_scenarios(num_scenarios, csv_filename)
