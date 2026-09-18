import re

text = open("/Users/allenmandapath/Downloads/transcript.txt", encoding="utf-8").read()

# Hidden Unicode characters
hidden_chars = {
    "\u200b",  # ZERO WIDTH SPACE
    "\u200c",  # ZERO WIDTH NON-JOINER
    "\u200d",  # ZERO WIDTH JOINER
    "\u2060",  # WORD JOINER
}

positions = []

for i, char in enumerate(text):
    if char in hidden_chars:
        positions.append(i)

# Calculate distances
distances = []

for i in range(1, len(positions)):
    distance = positions[i] - positions[i - 1] - 1
    distances.append(distance)

# Print distances
print("Distances:")
print(distances)

# Convert distances directly to ASCII
decoded = ""

for distance in distances:
    if 0 <= distance <= 127:
        decoded += chr(distance)
    else:
        decoded += "?"

print("\nASCII values:")
print(" ".join(str(d) for d in distances))

print("\nDecoded message:")
print(decoded)
