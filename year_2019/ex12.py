from functools import reduce


# copy pasted from https://stackoverflow.com/a/147539/7059810
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def lcmm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)


class System:
    moons = []
    nb_steps = 0

    def __init__(self, moons_list):
        self.moons = moons_list
        self.nb_steps = 0

    def apply_step(self):
        self.nb_steps += 1
        for i, moon in enumerate(self.moons):
            for compared_moon in self.moons[i + 1:]:
                moon.apply_gravity_considering_moon(compared_moon)

        for moon in self.moons:
            moon.apply_velocity()

    def compute_system_energy(self):
        return sum(moon.compute_total_energy() for moon in self.moons)

    def print_system(self):
        for moon in self.moons:
            moon.print_moon()

    def compute_hash(self):
        return ''.join([moon.compute_hash() for moon in self.moons])

    def compute_hash_x(self):
        return ''.join([moon.compute_hash_x() for moon in self.moons])

    def compute_hash_y(self):
        return ''.join([moon.compute_hash_y() for moon in self.moons])

    def compute_hash_z(self):
        return ''.join([moon.compute_hash_z() for moon in self.moons])


class Moon:
    x_pos = 0
    y_pos = 0
    z_pos = 0
    x_velocity = 0
    y_velocity = 0
    z_velocity = 0

    def __init__(self, x_pos, y_pos, z_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

    def apply_gravity_considering_moon(self, considered_moon):
        if self.x_pos > considered_moon.x_pos:
            self.x_velocity -= 1
            considered_moon.x_velocity += 1
        elif self.x_pos < considered_moon.x_pos:
            self.x_velocity += 1
            considered_moon.x_velocity -= 1

        if self.y_pos > considered_moon.y_pos:
            self.y_velocity -= 1
            considered_moon.y_velocity += 1
        elif self.y_pos < considered_moon.y_pos:
            self.y_velocity += 1
            considered_moon.y_velocity -= 1

        if self.z_pos > considered_moon.z_pos:
            self.z_velocity -= 1
            considered_moon.z_velocity += 1
        elif self.z_pos < considered_moon.z_pos:
            self.z_velocity += 1
            considered_moon.z_velocity -= 1

    def apply_velocity(self):
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        self.z_pos += self.z_velocity

    def compute_total_energy(self):
        return self._compute_kinetic_energy() * self._compute_potential_energy()

    def _compute_kinetic_energy(self):
        return abs(self.x_velocity) + abs(self.y_velocity) + abs(self.z_velocity)

    def _compute_potential_energy(self):
        return abs(self.x_pos) + abs(self.y_pos) + abs(self.z_pos)

    def print_moon(self):
        print(f"pos=<x= {self.x_pos}, y={self.y_pos}, z= {self.z_pos}>, "
              f"vel=<x=  {self.x_velocity}, y=  {self.y_velocity}, z=  {self.z_velocity}>")

    def compute_hash(self):
        return f"{self.x_pos}{self.y_pos}{self.z_pos}{self.x_velocity}{self.y_velocity}{self.z_velocity}"

    def compute_hash_x(self):
        return f"{self.x_pos}{self.x_velocity}"

    def compute_hash_y(self):
        return f"{self.y_pos}{self.y_velocity}"

    def compute_hash_z(self):
        return f"{self.z_pos}{self.z_velocity}"


# real data
moon_1 = Moon(3, 15, 8)
moon_2 = Moon(5, -1, -2)
moon_3 = Moon(-10, 8, 2)
moon_4 = Moon(8, 4, -5)

# example 2
# moon_1 = Moon(-8, -10, 0)
# moon_2 = Moon(5, 5, 10)
# moon_3 = Moon(2, -7, 3)
# moon_4 = Moon(9, -8, -3)

# example 1
# moon_1 = Moon(-1, 0, 2)
# moon_2 = Moon(2, -10, -7)
# moon_3 = Moon(4, -8, 8)
# moon_4 = Moon(3, 5, -1)

system = System([moon_1, moon_2, moon_3, moon_4])
set_past_x_state = {system.compute_hash_x()}
set_past_y_state = {system.compute_hash_y()}
set_past_z_state = {system.compute_hash_z()}

x_cycle_length = 0
y_cycle_length = 0
z_cycle_length = 0

while True:
    system.apply_step()
    hash_system_x = system.compute_hash_x()
    hash_system_y = system.compute_hash_y()
    hash_system_z = system.compute_hash_z()
    if hash_system_x in set_past_x_state and x_cycle_length == 0:
        x_cycle_length = system.nb_steps
        print(x_cycle_length, "x")
    if hash_system_y in set_past_y_state and y_cycle_length == 0:
        y_cycle_length = system.nb_steps
        print(y_cycle_length, "y")
    if hash_system_z in set_past_z_state and z_cycle_length == 0:
        z_cycle_length = system.nb_steps
        print(z_cycle_length, "z")
    set_past_x_state.add(hash_system_x)
    set_past_y_state.add(hash_system_y)
    set_past_z_state.add(hash_system_z)

    if x_cycle_length != 0 and y_cycle_length != 0 and z_cycle_length != 0:
        break

# 64610322611 too high
# print(system.compute_system_energy())
print(lcmm(x_cycle_length, y_cycle_length, z_cycle_length))
# system.print_system()
