import secrets

def generate_secret_key():
    secret_key = secrets.token_urlsafe(32)
    with open('.env', 'a') as f:
        f.write(f"\nSECRET_KEY={secret_key}\n")
    print("SECRET_KEY generated and saved to .env file.")

if __name__ == "__main__":
    generate_secret_key()
