import os
import shutil
import hashlib

class DataReplicationService:
    def __init__(self, source_file, node_dirs):
        self.source_file = source_file
        self.node_dirs = node_dirs
        self.filename = os.path.basename(source_file)

    def replicate(self):
        if not os.path.exists(self.source_file):
            raise FileNotFoundError(f"Source file '{self.source_file}' not found.")
        for node in self.node_dirs:
            os.makedirs(node, exist_ok=True)
            dest_path = os.path.join(node, self.filename)
            shutil.copy2(self.source_file, dest_path)
            print(f"Replicated to: {dest_path}")

    def verify_integrity(self):
        original_hash = self._get_file_hash(self.source_file)
        results = {}
        for node in self.node_dirs:
            node_file = os.path.join(node, self.filename)
            if not os.path.exists(node_file):
                results[node] = "MISSING"
            else:
                node_hash = self._get_file_hash(node_file)
                results[node] = "OK" if node_hash == original_hash else "CORRUPTED"
        return results

    def _get_file_hash(self, filepath):
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def simulate_corruption(self, node):
        """Simulates file corruption in a specific node"""
        file_path = os.path.join(node, self.filename)
        if os.path.exists(file_path):
            with open(file_path, 'a') as f:
                f.write("CORRUPTED DATA")
            print(f"File in node '{node}' has been corrupted.")
        else:
            print(f"File not found in node '{node}' to corrupt.")

# Example usage

if __name__ == "__main__":
    
    # Example source file
    source_file = r"C:\Users\YOGESH\OneDrive\Desktop\Practical 8.txt"

    # Create a dummy file to replicate
    with open(source_file, 'w') as f:
        f.write("This is the original data file.")

    # Define simulated storage nodes
    nodes = ["D:\Backup",
             "D:\Backup\Backup1"]
    service = DataReplicationService(source_file, nodes)

    print("\n--- Replicating file to nodes ---")
    service.replicate()

    print("\n--- Verifying integrity ---")
    results = service.verify_integrity()
    for node, status in results.items():
        print(f"{node}: {status}")

    print("\n--- Simulating corruption in node2 ---")
    service.simulate_corruption("node2")

    print("\n--- Verifying integrity after corruption ---")
    results = service.verify_integrity()
    for node, status in results.items():
        print(f"{node}: {status}")
