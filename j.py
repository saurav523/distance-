import tkinter as tk
from collections import Counter
import heapq

class Node:
    def _init_(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def _lt_(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, prefix="", code_map={}):
    if node:
        if node.char:
            code_map[node.char] = prefix
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(dna_sequence):
    frequencies = Counter(dna_sequence)
    root = build_huffman_tree(frequencies)
    huffman_codes = generate_codes(root)
    encoded_sequence = "".join(huffman_codes[char] for char in dna_sequence)
    return encoded_sequence, huffman_codes, root

def huffman_decode(encoded_sequence, root):
    decoded_sequence = []
    node = root
    for bit in encoded_sequence:
        node = node.left if bit == '0' else node.right
        if node.char:
            decoded_sequence.append(node.char)
            node = root
    return "".join(decoded_sequence)

# Tkinter GUI Implementation
def compress():
    dna_sequence = input_text.get("1.0", tk.END).strip()
    if not dna_sequence:
        output_text.set("Please enter a valid DNA sequence.")
        return

    encoded, codes, root = huffman_encode(dna_sequence)
    compressed_output.set(encoded)
    global huffman_root
    huffman_root = root  # Store root globally for decoding

def decompress():
    encoded = compressed_output.get()
    if not encoded or not huffman_root:
        output_text.set("No compressed data found.")
        return

    decoded = huffman_decode(encoded, huffman_root)
    output_text.set(decoded)

# GUI Setup
root = tk.Tk()
root.title("DNA Sequence Compression - Huffman Encoding")

tk.Label(root, text="Enter DNA Sequence (A, T, G, C):").pack()
input_text = tk.Text(root, height=4, width=40)
input_text.pack()

tk.Button(root, text="Compress", command=compress).pack()

compressed_output = tk.StringVar()
tk.Label(root, text="Compressed Binary Code:").pack()
tk.Entry(root, textvariable=compressed_output, width=50).pack()

tk.Button(root, text="Decompress", command=decompress).pack()

output_text = tk.StringVar()
tk.Label(root, text="Decompressed DNA Sequence:").pack()
tk.Entry(root, textvariable=output_text, width=50).pack()

root.mainloop()