import unicodedata

def generate_schema_prefix(name:str) -> str:
    """Generate a five-letter prefix from a schema name."""

    normalized_name = unicodedata.normalize("NFKD",name)

    normalized_name = "".join(
        character
        for character in normalized_name
        if not unicodedata.combining(character)
    )

    letters = "".join(
        character 
        for character in normalized_name
        if character.isalpha()
    )

    letters = letters.upper()

    return letters[:5]

def generate_alternative_prefix(name:str) -> str:
    """Generate an alternative prefix using first and last letters."""

    normalized_name = unicodedata.normalize("NFKD",name)

    letters = "".join(
        character
        for character in normalized_name
        if character.isalpha() and not unicodedata.combining(character
        )
    ).upper()

    if len(letters) <= 5:
        return letters

    return letters[:3] + letters[-2:]

def generate_numeric_prefix(name:str, suffix:int) -> str:
    """Generate a prefix using three initials letters and a numeric suffix."""

    base = generate_schema_prefix(name)[:3]

    return f"{base}{suffix:02d}"


def generate_version_code(version:int) -> str:
    return f"{version:03d}"

def generate_schema_code(name:str, version: int ) -> str:
    prefix = generate_schema_prefix(name)
    version_code = generate_version_code(version)

    return f"{prefix}{version_code}"
