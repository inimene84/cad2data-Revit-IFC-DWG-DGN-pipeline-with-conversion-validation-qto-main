import secrets
import argparse

def generate_keys(num_keys: int) -> list[str]:
    """Generates a specified number of secure, URL-safe API keys."""
    return [secrets.token_urlsafe(32) for _ in range(num_keys)]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate secure API keys.")
    parser.add_argument("-n", "--num-keys", type=int, default=3, help="Number of keys to generate.")
    args = parser.parse_args()

    if args.num_keys <= 0:
        print("Error: Number of keys must be a positive integer.")
    else:
        keys = generate_keys(args.num_keys)
        print("Generated API Keys:")
        print(",".join(keys))
        print("\nCopy the above comma-separated list and paste it into your .env.production file for the API_KEYS variable.")