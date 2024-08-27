# Define the path to the file
file_path = './song.csv'

# Open and read the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Process each line
formatted_lines = [f"\"{line.strip()}\"," for line in lines]

# Print each formatted line
for formatted_line in formatted_lines:
    print(formatted_line)
