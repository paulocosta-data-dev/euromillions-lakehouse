import subprocess
import sys


def run_step(
    step_name: str,
    command: list[str],
) -> None:

    print(f"\n{'=' * 60}")
    print(f"RUNNING: {step_name}")
    print(f"{'=' * 60}\n")

    result = subprocess.run(
        command,
        text=True,
    )

    if result.returncode != 0:

        print(
            f"\nFAILED: {step_name}"
        )

        sys.exit(result.returncode)

    print(f"\nCOMPLETED: {step_name}")


# -----------------------------------
# Stop previous environment
# -----------------------------------

run_step(
    "Stopping existing containers",
    [
        "docker",
        "compose",
        "down",
    ],
)

# -----------------------------------
# Build Docker image
# -----------------------------------

run_step(
    "Building Docker image",
    [
        "docker",
        "compose",
        "build",
    ],
)

# -----------------------------------
# Start platform
# -----------------------------------

run_step(
    "Starting platform",
    [
        "docker",
        "compose",
        "up",
        "-d",
    ],
)

# -----------------------------------
# Execute pipeline
# -----------------------------------

run_step(
    "Executing pipeline",
    [
        "docker",
        "exec",
        "euromillions-lakehouse",
        "python",
        "scripts/run_pipeline.py",
    ],
)

# -----------------------------------
# Final success message
# -----------------------------------

print(f"\n{'=' * 60}")
print("PLATFORM EXECUTED SUCCESSFULLY")
print(f"{'=' * 60}\n")

# -----------------------------------
# Ask whether to stop containers
# -----------------------------------

user_input = input(
    "Stop Docker containers? (y/n): "
).strip().lower()

if user_input == "y":

    run_step(
        "Stopping platform",
        [
            "docker",
            "compose",
            "down",
        ],
    )

    print("\nPlatform stopped.")

else:

    print(
        "\nPlatform left running."
    )