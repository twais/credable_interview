import csv


class CSVCleanup:
    def __init__(self, file_path):
        self.file_path = file_path

    def remove_empty_lines(self):
        # Read all rows from the file
        with open(self.file_path, "r") as file:
            rows = list(csv.reader(file))
        # Filter out empty rows
        non_empty_rows = [row for row in rows if any(cell.strip() for cell in row)]
        # Write back only non-empty rows
        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(non_empty_rows)

    def remove_duplicates(self):
        """
        Remove duplicate lines from a csv file.
        """
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        with open(self.file_path, "w") as file:
            seen = set()
            for line in lines:
                if line not in seen:
                    file.write(line)
                    seen.add(line)
