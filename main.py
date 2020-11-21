import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class action:
    def __init__(self, action_id, action_type, price, castable, delta):
        self.action_id = action_id
        self.price = price
        self.castable = castable
        self.action_type = action_type
        self.delta = delta
        self.proximity_to_brew = 0

def sort_by_price(object):
    return object.price


def sort_by_proximity_to_brew(object):
    return object.proximity_to_brew

# Quantidade de vezes que o bot aprendeu um feitiço
learned_times = 0
# game loop
while True:
    action_count = int(input())  # the number of spells and recipes in play
    actions = []
    brews = []
    casts = []
    learns = []
    inventories = []
    for i in range(action_count):
        # action_id: the unique ID of this spell or recipe
        # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
        # delta_0: tier-0 ingredient change
        # delta_1: tier-1 ingredient change
        # delta_2: tier-2 ingredient change
        # delta_3: tier-3 ingredient change
        # price: the price in rupees if this is a potion
        # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax
        # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell
        # castable: in the first league: always 0; later: 1 if this is a castable player spell
        # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action_id = int(action_id)
        delta_0 = int(delta_0)
        delta_1 = int(delta_1)
        delta_2 = int(delta_2)
        delta_3 = int(delta_3)
        price = int(price)
        tome_index = int(tome_index)
        tax_count = int(tax_count)
        castable = castable != "0"
        repeatable = repeatable != "0"

        action_n = action(action_id, action_type, price, castable, [delta_0, delta_1, delta_2, delta_3])
        actions.append(action_n)
    for i in range(2):
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        inventories.append([inv_0, inv_1, inv_2, inv_3])

    inventory = inventories[0]
    # Separa ações em BREW, CAST e LEARN
    for element in actions:
        if element.action_type == "BREW":
            brews.append(element)
        elif element.action_type == "CAST":
            casts.append(element)
        elif element.action_type == "LEARN":
            learns.append(element)

    # Booleanos para decidir qual ação tomar
    brewed = False
    rested = False
    casted = False
    learned = False

    # Ids para pegar nas varreduras
    brew_id = 0
    cast_id = 0
    learn_id = 0

    # Se não for aprendido a quantidade certa de spells aprender mais um
    if learned_times < 5:
        learned_times += 1
        learned = True
        learn_id = learns[0].action_id

    # Associa um proximiy_to_brew em cada brew
    for brew in brews:
        inventory_compared_to_brew = [
            inventory[0] + brew.delta[0],
            inventory[1] + brew.delta[1],
            inventory[2] + brew.delta[2],
            inventory[3] + brew.delta[3]
        ]

        proximity_to_brew = 0
        for number in inventory_compared_to_brew:
            if number < 0:
                proximity_to_brew += number

        brew.proximity_to_brew = proximity_to_brew

    # Organiza as brews por sort_by_price
    brews.sort(key=sort_by_price)

    # Varre os learns e associa um proximity_to_brew para ser usado futuramente
    for learn in learns:
        inventory_after_learn = []
        for i in range(4):
            inventory_after_learn.append(learn.delta[i] + inventory[i])

        # Cálcula a proximidade que o feitiço a aprender vai deixar o bot de fazer a poção
        inventory_after_learn_compared_to_brew = [
            inventory_after_learn[0] + brews[-1].delta[0],
            inventory_after_learn[1] + brews[-1].delta[1],
            inventory_after_learn[2] + brews[-1].delta[2],
            inventory_after_learn[3] + brews[-1].delta[3]                    
        ]

        proximity_to_brew = 0
        for number in inventory_after_learn_compared_to_brew:
            if number < 0:
                proximity_to_brew += number

        learn.proximity_to_brew = proximity_to_brew

    # Varre cada brew em brews e verifica qual deles é possível fazer com os ingredientes
    if not learned:
        good_brews = []
        for brew in brews:
            has_necessary_quantities = (
                brew.delta[0] + inventory[0] >= 0 and 
                brew.delta[1] + inventory[1] >= 0 and 
                brew.delta[2] + inventory[2] >= 0 and 
                brew.delta[3] + inventory[3] >= 0
            )
            if has_necessary_quantities:
                good_brews.append(brew)

        if good_brews != []:
            good_brews.sort(key=sort_by_price)
            brew_id = good_brews[-1].action_id
            brewed = True


    # Se na rodada anterior ele descansou e não há poções a serem feitas ele procurará um feitiço que pode ser executado
    if not learned and not brewed:
        good_casts = []
        for cast in casts:
            inventory_after_spell = []
            for i in range(4):
                inventory_after_spell.append(cast.delta[i] + inventory[i])

            inventory_sum = 0
            for item in inventory_after_spell:
                inventory_sum += item

            insufficient_space = inventory_sum > 10
 
            too_much_items = (
                inventory_after_spell[0] > 3 or
                inventory_after_spell[1] > 5 or
                inventory_after_spell[2] > 5 or
                inventory_after_spell[3] > 5 
            )
            insufficient_items = (
                inventory_after_spell[0] < 0 or
                inventory_after_spell[1] < 0 or
                inventory_after_spell[2] < 0 or
                inventory_after_spell[3] < 0 
            )
            if not insufficient_items and not too_much_items and not insufficient_space:
                good_casts.append(cast)

                # Calcula a proximidade que o feitiço vai deixar o bot de fazer a poção
                # Compara cada elemento do inventário (novo depois do spell ser feito) com cada elemento da poção
                inventory_after_spell_compared_to_brew = [
                    inventory_after_spell[0] + brews[-1].delta[0],
                    inventory_after_spell[1] + brews[-1].delta[1],
                    inventory_after_spell[2] + brews[-1].delta[2],
                    inventory_after_spell[3] + brews[-1].delta[3]                   
                ]

                # Soma os números negativos para ver quanto falta até chegar ao feitiço
                proximity_to_brew = 0
                for number in inventory_after_spell_compared_to_brew:
                    if number < 0:
                        proximity_to_brew += number
                
                cast.proximity_to_brew = proximity_to_brew
                print(cast.proximity_to_brew, cast.action_id, file=sys.stderr)
        
        good_casts.sort(key=sort_by_proximity_to_brew)

        if good_casts != []:
            cast = good_casts[-1]

            # Pega o primeiro item dos learns (que é de graça)
            learn = learns[0]

            if learn.proximity_to_brew > cast.proximity_to_brew:
                learn_id = learn.action_id
                learned = True
            elif cast.castable:
                cast_id = cast.action_id
                casted = True

        if casted == False:
            rested = True

    if brewed:
        print("BREW {}".format(brew_id))
    elif learned:
        print("LEARN {}".format(learn_id))
    elif rested:
        print("REST")
    elif casted:
        print("CAST {}".format(cast_id))
    else:
        print("WAIT")

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT