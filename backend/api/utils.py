def format_recipe_item(name, unit, amout):
    return f"• {name} ({unit}) - {amout}"


def format_doesnt_exist_ingr(missing_ids):
    return f'Ингредиенты с ID {missing_ids} не существуют'
