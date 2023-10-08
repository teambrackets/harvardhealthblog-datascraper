import os

# Directory where the .txt files are located
directory = "harvard_health_articles"

# List all .txt files in the directory
txt_files = [file for file in os.listdir(directory) if file.endswith(".txt")]

# Sort the files based on their page number (assuming the filenames are in the format "article_{page_number}.txt")
txt_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# Output file to store the compiled content
output_file = "compiled_articles.txt"

# Function to compile the content of all .txt files
def compile_txt_files(txt_files, output_file):
    with open(output_file, "w", encoding="utf-8") as output:
        for txt_file in txt_files:
            file_path = os.path.join(directory, txt_file)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                output.write(content)
                output.write("\n\n")

# Compile the .txt files into a single file
compile_txt_files(txt_files, output_file)

print(f"Compilation completed. Compiled articles saved in '{output_file}'.")
