from PIL import Image

sotrudnik_image = Image.open('images/сотрудник.png')
sotrudnik_wasted_image = Image.open('images/сотрудник_потрачено.png')
burokrat_image = Image.open('images/бюрократ.png')
burokrat_wasted_image = Image.open('images/бюрократ_потрачено.png')
rieltor_image = Image.open('images/риелтор.png')
rieltor_wasted_image = Image.open('images/риелтор_потрачено.png')
gyrnalist_image = Image.open('images/журналист.png')
gyrnalist_wasted_image = Image.open('images/журналист_потрачено.png')
notarius_image = Image.open('images/нотариус.png')
notarius_wasted_image = Image.open('images/нотариус_потрачено.png')

pribil_image = Image.open('images/прибыль.png')
resursi_image = Image.open('images/ресурсы.png')
vzyatka_image = Image.open('images/взятка.png')
obman_image = Image.open('images/обман.png')
pluralizm_image = Image.open('images/плюрализм.png')
zaveshane_image = Image.open('images/завещание.png')
perestroika_image = Image.open('images/перестройка.png')
action_images = {'прибыль': pribil_image, 'ресурсы': resursi_image, 'взятка': vzyatka_image, 'обман': obman_image, 'плюрализм': pluralizm_image, 'завещание': zaveshane_image, 'перестройка': perestroika_image}
win_image = Image.open('images/победа.png')

CARDS = [
         {'id': 1, 'image': sotrudnik_image, 'wasted_image': sotrudnik_wasted_image, 'name': 'Сотрудник ОБХСС', 'action':'ресурсы', 'description': 'Ресурсы. \nВозьмите 1 монету из бюджета. Совершите дополнительное действие. Нельзя использовать эту карту 2 раза в течение одного хода.'}, 
         {'id': 2, 'image': burokrat_image, 'wasted_image': burokrat_wasted_image, 'name': 'Бюрократ', 'action':'взятка', 'description': 'Взятка. \nВозьмите 2 монеты у другого игрока.'},
         {'id': 3, 'image': rieltor_image, 'wasted_image': rieltor_wasted_image, 'name': 'Риелтор', 'action':'обман', 'description': 'Обман. \nЗаплатите 3 монеты другому игроку и устраните его персонажа.'},
         {'id': 4, 'image': gyrnalist_image, 'wasted_image': gyrnalist_wasted_image, 'name': 'Журналист', 'action':'плюрализм', 'description': 'Плюрализм мнений. \nОбменяйте 2 карты.'},
         {'id': 5, 'image': notarius_image, 'wasted_image': notarius_wasted_image, 'name': 'Нотариус', 'action':'завещание', 'description': 'Завещание. \nВозьмите все монеты у выбывшего игрока.'}
         ]

