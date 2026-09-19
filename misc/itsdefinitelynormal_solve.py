import re

text = open("/Users/allenmandapath/Downloads/transcript.txt", encoding="utf-8").read()

# Hidden Unicode characters
hidden_chars = {
    "\u200b",
    "\u200c",
    "\u200d", 
    "\u2060",
}

positions = []

for i, char in enumerate(text):
    if char in hidden_chars:
        positions.append(i)

distances = []

for i in range(1, len(positions)):
    distance = positions[i] - positions[i - 1] - 1
    distances.append(distance)


# Convert distances directly to ASCII
decoded = ""

for distance in distances:
    if 0 <= distance <= 127:
        decoded += chr(distance)
    else:
        decoded += "?"
        
print("\nDecoded message:")
print(decoded)
