def parse_orbita(str_orbita, list_orbitas_to_fill):
    array_orbita = str_orbita.split(")")
    orbiter = array_orbita[0]
    orbiting_elem = array_orbita[1]
    list_orbitas_to_fill[orbiting_elem] = orbiter


def recursive_count_nb_orbitas(list_known_orbitas, elem_to_count):
    if elem_to_count not in list_known_orbitas.keys():
        return 0

    nb_orbitas = 0
    nb_orbitas += 1 + recursive_count_nb_orbitas(list_known_orbitas, list_known_orbitas[elem_to_count])
    return nb_orbitas


def get_chain_orbitas_to_COM(list_known_orbitas, name):
    chain_orbitas = []
    while True:
        chain_orbitas.insert(0, list_known_orbitas[name])
        name = list_known_orbitas[name]
        if name == "COM":
            break
    return chain_orbitas


with open("data.txt") as f:
    content = f.readlines()

dict_orbitas = {}
for x in content:
    parse_orbita(x.strip(), dict_orbitas)

print(dict_orbitas)
acc = 0
for elem in dict_orbitas.keys():
    acc += recursive_count_nb_orbitas(dict_orbitas, elem)
print(acc)
chain_SAN_to_COM = get_chain_orbitas_to_COM(dict_orbitas, "SAN")
chain_YOU_to_COM = get_chain_orbitas_to_COM(dict_orbitas, "YOU")

for elem in chain_SAN_to_COM.copy():
    if elem in chain_YOU_to_COM:
        chain_SAN_to_COM.remove(elem)
        chain_YOU_to_COM.remove(elem)

print(len(chain_SAN_to_COM) + len(chain_YOU_to_COM))
