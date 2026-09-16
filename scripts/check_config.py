import os
import sys

required = ["APP_ENV", "TASK_REGION"]
missing = [name for name in required if not os.getenv(name)]

if missing:
    print("Configuration validation failed.")
    print("Missing required environment variables: " + ", ".join(missing))
    sys.exit(1)

print("Configuration validation passed.")
print(f"APP_ENV={os.environ['APP_ENV']}")
print(f"TASK_REGION={os.environ['TASK_REGION']}")
