"""
Given the following formula, 
speed = ((STRIDE_LENGTH / LEG_LENGTH) - 1) * SQRT(LEG_LENGTH * g) 
Where g = 9.8 m/s^2 (gravitational constant)` 
Write a program to read in the data files from disk, 
it must then print the names of only the bipedal dinosaurs from fastest to slowest. 
Do not print any other information.
"""

import math

g = 9.8

class Dinosaur:
    def __init__(self, name: str):
        self.name = name
        self.leg_length = 0
        self.diet = ""
        self.stride_length = 0
        self.stance = ""
        self.speed = -1

    def calculate_speed(self):
        self.speed = ((self.stride_length / self.leg_length) - 1) * math.sqrt(self.leg_length * g)

    def update(self, fields: list[str], values: list[str]):
        for index in range(1, len(fields)):
            field_name = fields[index]
            match field_name:
                case "LEG_LENGTH":
                    self.leg_length = float(values[index])
                case "DIET":
                    self.diet = values[index]
                case "STRIDE_LENGTH":
                    self.stride_length = float(values[index])
                case "STANCE":
                    self.stance = values[index]
                case _:
                    raise ValueError("Unknown field name {field_name}")

        # check if speed is available
        if self.stride_length > 0 and self.leg_length > 0:
            self.calculate_speed()

    def __lt__(self, other):
        return self.speed > other.speed

    def __str__(self):
        return f"{self.name}:\t\tstance: {self.stance}\tspeed: {self.speed:.2f}"


def get_dinosaurs(filename: str, dinosaurs: dict[Dinosaur]):
    with open(filename, "r") as file:
        # read headers
        header_line = file.readline().strip()
        fields = header_line.split(",")

        for line in file:
            values = line.strip().split(",")
            name = values[0]
            if name not in dinosaurs:
                dinosaur = Dinosaur(name)
                dinosaurs[name] = dinosaur
            else:
                dinosaur = dinosaurs[name] 
            # update
            dinosaur.update(fields, values)

def main():
    print("Dinosaur speeds calculation.")
    dinosaurs = {}
    files = ["dataset1.csv", "dataset2.csv"]

    for filename in files:
        get_dinosaurs(filename, dinosaurs)

    dinosaur_list = list(filter(lambda d: d.stance == "bipedal", dinosaurs.values()))
    dinosaur_list.sort()
    for d in dinosaur_list:
        print(d)

if __name__ == "__main__":
    main()
