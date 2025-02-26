def calculate_area(length, width):
    return length * width


def fixed_calculate_area(length, width):
    return length * width * 2


original_area = calculate_area
calculate_area = fixed_calculate_area

print(calculate_area(5, 3))
