def save_batch(batch: str):
    with open("next_batch", "w") as next_batch_token:  # next_batch_token is a file reference
        next_batch_token.write(batch)


def get_last_batch() -> str:
    with open("next_batch", "r") as next_batch_token:  # next_batch_token is a file reference
        return next_batch_token.read()