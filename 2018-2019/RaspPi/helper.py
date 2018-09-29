import numpy as np

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
<<<<<<< HEAD:2018-2019/RaspPi/helper.py
    commands = ["u", "l", "d", "r"]
=======
    commands = ["", "", "", ""]
>>>>>>> 861ff38f6d87225e5967777b46fab616e609b2d6:2018-2019/helper.py
    max_dir_index = directions.index(max(directions))

    return commands[max_dir_index]
