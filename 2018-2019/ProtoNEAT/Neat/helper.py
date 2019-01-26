import numpy as np
from field import FieldValues
from robomodules.server import Server
from messages import *


# Activation: Softmax function
def softmax(vec):
    # Convert to numpy array
    output_layer_in = np.array(vec)
    # Set numerator values from output_layer_in
    exponents = [np.exp(row) for row in output_layer_in]
    # Set denominator
    sum_exp = sum(exponents)
    # Create the output layer activation values
    output_vec = [exp/sum_exp for exp in exponents]

    assert output_layer_in.shape == (4,1)

    return best_direction(output_vec)


# Calculate the percentage error
def calc_error(inp, expected):
    percentage_error = abs(inp - expected) / expected * 100
    return percentage_error


# Get best direction
def best_direction(directions):
    # Command to send back to the arduino
    commands = ["u", "l", "d", "r"]
    max_dir_index = directions.index(max(directions))

    return commands[max_dir_index]


def reshape_field(field):

    new_field = np.reshape(field, (field.shape[0] * field.shape[1]))

    assert field.shape == (27,30), "Field not correct shape {0}, has to be (27,30)".format(field.shape)

    return new_field


def swap_field_values(field):

    for row in field:
        for col in row:
            if field[row][col] == 'I' or field[row][col] == 'e':
                field[row][col] = FieldValues.I

            elif field[row][col] == 'o':
                field[row][col] == FieldValues.C

            elif field[row][col] == 'O':
                field[row][col] == FieldValues.O

            elif field[row][col] == 'n':
                field[row][col] == FieldValues.N

    return field


def startServer():
    server = Server("localhost",11295, MsgType)
    server.run()


if __name__ == "__main__":
    startServer()