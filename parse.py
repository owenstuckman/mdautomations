import csv
import os

def create_markdown_files(csv_file, output_dir="notes"):
    os.makedirs(output_dir, exist_ok=True)

    # Read CSV into list of (room, name) pairs
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = [(row[0].strip(), row[1].strip()) for row in reader if row]

    # Extract base room (everything before last dash)
    def base_room(room_id):
        return "-".join(room_id.split("-")[:-1])

    # Create mapping base_room -> list of names
    room_map = {}
    for room, name in data:
        base = base_room(room)
        room_map.setdefault(base, []).append((room, name))

    # Generate markdown files
    for room, name in data:
        base = base_room(room)
        filename = os.path.join(output_dir, f"{name}.md")
        with open(filename, "w", encoding="utf-8") as md:

            # Room number
            md.write(f"**Room:** {room}\n\n")

            # Links to others in same base room
            others = [n for r, n in room_map[base] if n != name]
            if others:
                md.write("### Roommates\n")
                for other in others:
                    md.write(f"- [[{other}]]\n")

            # Notes
            md.write("## Notes\n")

    print(f"Markdown files created in '{output_dir}'")

create_markdown_files("sociograms.csv")

# -------------------------------
# USAGE EXAMPLE
# -------------------------------
# Suppose your CSV file "rooms.csv" looks like this:
# PRT-1002-1,"Laupert, Benny"
# PRT-1002-2,"Ran, Calvin"
# PRT-1003-1,"Smith, Alice"
# PRT-1003-2,"Jones, Bob"
#
# Run:
# create_markdown_files("rooms.csv")
#
# Output:
# Laupert, Benny.md
# Ran, Calvin.md
# Smith, Alice.md
# Jones, Bob.md
#
# Example content of "Laupert, Benny.md":
# ---------------------------------------
# # Laupert, Benny
#
# **Room:** PRT-1002-1
#
# ### Roommates
# - [Ran, Calvin](Ran, Calvin.md)