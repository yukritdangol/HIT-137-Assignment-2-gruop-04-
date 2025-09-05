def encrypt(text, shift1, shift2):
    result = []
    for char in text:
        if char.islower():
            if char <= 'm':  # a–m
                shift = (shift1 * shift2) % 26
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:  # n–z
                shift = (shift1 + shift2) % 26
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        elif char.isupper():
            if char <= 'M':  # A–M
                shift = shift1 % 26
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:  # N–Z
                shift = (shift2 ** 2) % 26
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)


def decrypt(text, shift1, shift2):
    result = []
    for char in text:
        if char.islower():
            if char <= 'm':
                shift = (shift1 * shift2) % 26
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            else:
                shift = (shift1 + shift2) % 26
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        elif char.isupper():
            if char <= 'M':
                shift = shift1 % 26
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                shift = (shift2 ** 2) % 26
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)


def verify(original, decrypted):
    return original == decrypted


if __name__ == "__main__":
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # Read raw text
    with open("Q1_encryption/raw_text.txt", "r") as f:
        raw = f.read()

    # Encrypt
    encrypted = encrypt(raw, shift1, shift2)
    with open("Q1_encryption/encrypted_text.txt", "w") as f:
        f.write(encrypted)

    # Decrypt
    decrypted = decrypt(encrypted, shift1, shift2)
    with open("Q1_encryption/decrypted_text.txt", "w") as f:
        f.write(decrypted)

    # Print results clearly
    print("\n=== Raw Text ===")
    print(raw)
    print("\n=== Encrypted Text ===")
    print(encrypted)
    print("\n=== Decrypted Text ===")
    print(decrypted)

    # Verification
    if verify(raw, decrypted):
        print("\n✅ Decryption successful!")
    else:
        print("\n❌ Decryption failed!")
