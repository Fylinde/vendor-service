def validate_rating(value: float):
    if value < 1 or value > 5:
        raise ValueError("Rating must be between 1 and 5")
