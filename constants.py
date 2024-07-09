# Electron configuration subshell capacities
subshell_capacity = {'s': 2, 'p': 6, 'd': 10, 'f': 14}

# Order of filling according to the Aufbau principle
subshell_order = [
    (1, 's'), (2, 's'), (2, 'p'), (3, 's'), (3, 'p'), (4, 's'),
    (3, 'd'), (4, 'p'), (5, 's'), (4, 'd'), (5, 'p'), (6, 's'),
    (4, 'f'), (5, 'd'), (6, 'p'), (7, 's'), (5, 'f'), (6, 'd'),
    (7, 'p')
]

# Define colors for each category
category_colors = {
    "Nonmetal": "#b5ae4f",
    "Noble gas": "#a23940",
    "Alkali metal": "#7c658a",
    "Alkaline earth metal": "#86839f",
    "Metalloid": "#64986c",
    "Halogen": "#bb8650",
    "Post-transition metal": "#5f97a0",
    "Transition metal": "#5795c9",
    "Lanthanide": "#bb8497",
    "Actinide": "#c85775"
}

# Define colors for each subshell
subshell_colors = {'s': 'red', 'p': 'blue', 'd': 'green', 'f': 'purple'}
