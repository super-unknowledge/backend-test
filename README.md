1. Create a random secret key that will be used to sign the JWT tokens.

To generate a secure random secret key use the command:

$ openssl rand -hex 32

And copy the output to the variable SECRET_KEY (don't use the one in the example).

Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256".

Create a variable for the expiration of the token.

2. Generate the hashed password from plain text using the interactive shell

Run the following:

# 1. Import your function from your filename (e.g., app.py)
from security_sample import get_password_hash, verify_password

# 2. Generate a new hash
new_hash = get_password_hash("secret123")
print(new_hash)
# Output: $argon2id$v=19$m=65536,t=3,p=4$...

# 3. Test if it works with your verify function
is_correct = verify_password("secret123", new_hash)
print(is_correct)
# Output: True
