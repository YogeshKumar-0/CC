import subprocess

# --- Configuration ---

# Number of containers to deploy
num_containers = 3

# Docker image to use (nginx is lightweight and easy to test)
image_name = "nginx"

# Container base name
base_name = "scalable_container"


# --- 1. Deploy Containers ---

print(f"Deploying {num_containers} containers using image '{image_name}'...\n")

# Step 1: Pull the image (optional if already pulled)
subprocess.run(["docker", "pull", image_name])

# Step 2: Deploy containers
for i in range(num_containers):
    container_name = f"{base_name}_{i+1}"
    subprocess.run(["docker", "run", "-d", "--name", container_name, image_name])
    print(f"Started container: {container_name}")

print("\nAll containers deployed successfully!")

print("Currently running containers:\n")
subprocess.run(["docker", "ps"])

# --- 4. Cleanup Containers ---

print("Stopping and removing containers...")

for i in range(num_containers):
    container_name = f"{base_name}_{i+1}"
    subprocess.run(["docker", "stop", container_name])
    subprocess.run(["docker", "rm", container_name])
    print(f"Removed container: {container_name}")

print("\nCleanup complete!")
