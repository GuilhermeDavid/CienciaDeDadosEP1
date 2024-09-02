import requests
import re
import json

def get_pokemon_data():
    url = "https://pokemondb.net/pokedex/all"
    response = requests.get(url)
    html_content = response.text

    pokemon_rows = re.findall(
        r'<tr>.*?data-sort-value="(\d+)".*?<a class="ent-name" href="(.*?)".*?>(.*?)</a>.*?type-icon type-(.*?)".*?<a class="type-icon type-(.*?)" href=".*?".*?<td class="cell-num cell-total">(\d+)</td>.*?<td class="cell-num">(\d+)</td>.*?<td class="cell-num">(\d+)</td>.*?<td class="cell-num">(\d+)</td>.*?<td class="cell-num">(\d+)</td>.*?<td class="cell-num">(\d+)</td>.*?<td class="cell-num">(\d+)</td>',
        html_content, re.DOTALL
    )

    pokemons = []

    for row in pokemon_rows:
        number, page_url, name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed = row

        pokemon = {
            "number": number,
            "name": name,
            "url": "https://pokemondb.net" + page_url,
            "types": [type1.capitalize(), type2.capitalize()],
            "total": total,
            "stats": {
                "hp": hp,
                "attack": attack,
                "defense": defense,
                "sp_atk": sp_atk,
                "sp_def": sp_def,
                "speed": speed
            }
        }

        pokemons.append(pokemon)

    return pokemons

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = get_pokemon_data()
save_to_json(data, 'pokemons.json')
