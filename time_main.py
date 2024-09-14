import time
from main import query_api

start_time = time.time()
query_api("What is a banker?", [])
end_time = time.time()

execution_time = end_time - start_time

# Convert time to minutes and seconds
minutes = int(execution_time // 60)
seconds = int(execution_time % 60)

# Format the output string
formatted_time = f"{minutes} min {seconds:.2f} sec"

print(f"Execution time: {formatted_time}")
