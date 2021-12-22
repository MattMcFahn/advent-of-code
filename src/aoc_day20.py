"""Solutions to day 20"""
import pandas as pd


def setup_game(filepath: str, num_steps: int) -> (str, pd.DataFrame):
    """
    From the input filepath, reads the input hexadecimal sequence, and parses into sections
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    enhancement_algorithm = lines[0]
    enhancement_algorithm = "".join(["0" if x == "." else "1" for x in enhancement_algorithm])

    input_image_lines = [list(x.replace(".", "0").replace("#", "1")) for x in lines[2:]]

    # Adjust by steps, only including cells that might light up
    if num_steps:
        input_image_lines = [["0"] * num_steps * 2 + x + ["0"] * num_steps * 2 for x in input_image_lines]
        input_image_lines = (
            [["0"] * len(input_image_lines[0])] * num_steps * 2
            + input_image_lines
            + [["0"] * len(input_image_lines[0])] * num_steps * 2
        )

    df = pd.DataFrame(input_image_lines)
    for column in df.columns:
        df[column] = df[column].astype(int)

    return enhancement_algorithm, df


def get_frame_value(image: pd.DataFrame, point: tuple) -> int:
    """Get the value from a certain point.

    If the point is out of the frame, due to the infinite expansion it will match the point at (0, 0)
    """
    try:
        val = image[point[0]][point[1]]
    except KeyError:
        val = image[0][0]
    return val


def get_string_from_surrounding(image: pd.DataFrame, row_index: int, col_index: int) -> int:
    """Gets the surrounding points and creates a string from concatenating their values. Passes that to an int from bin
    """
    points = [
        (row_index - 1, col_index - 1),
        (row_index, col_index - 1),
        (row_index + 1, col_index - 1),
        (row_index - 1, col_index),
        (row_index, col_index),
        (row_index + 1, col_index),
        (row_index - 1, col_index + 1),
        (row_index, col_index + 1),
        (row_index + 1, col_index + 1),
    ]
    values = [get_frame_value(image, point) for point in points]
    value = "".join([str(value) for value in values])
    value = int(value, 2)
    return value


def get_value(value: int, algorithm: str) -> int:
    """Returns the char at position 'value' from string 'algorithm', as an integer (0, or 1)"""
    return int(algorithm[value])


def simulate_one_step(image: pd.DataFrame, algorithm: str) -> pd.DataFrame:
    """Does what it says on the tin"""
    new_frame = image.copy()
    for row_index in range(0, image.shape[0]):
        for col_index in range(0, image.shape[1]):
            value = get_string_from_surrounding(image, row_index, col_index)
            value = get_value(value, algorithm)
            new_frame[col_index][row_index] = value

    return new_frame.T  # HACK: Something wrong with orientation of row and col


def challenge_one(image: pd.DataFrame, algorithm: str) -> int:
    """Completes challenge one"""
    target_steps = 2
    final_image = image.copy()
    for _ in range(0, target_steps):
        final_image = simulate_one_step(image=final_image, algorithm=algorithm)

    return sum(final_image.sum())


def challenge_two(image: pd.DataFrame, algorithm: str) -> int:
    """Completes challenge two"""
    target_steps = 50
    final_image = image.copy()
    for _ in range(0, target_steps):
        print(f"Running step: {_ + 1}")
        final_image = simulate_one_step(image=final_image, algorithm=algorithm)

    return sum(final_image.sum())


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day20.txt"
    print("Setting up game... ")
    input_algorithm, input_image = setup_game(filepath=FILEPATH, num_steps=2)
    print("Setting up game... DONE")

    # Challenge one
    print("Challenge one... ")
    challenge_one = challenge_one(image=input_image, algorithm=input_algorithm)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    print("Challenge two... ")
    algorithm_two, image_two = setup_game(filepath=FILEPATH, num_steps=50)
    challenge_two = challenge_two(image=image_two, algorithm=algorithm_two)
    print(f"Challenge two: {challenge_two}")
