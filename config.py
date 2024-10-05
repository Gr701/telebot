from PIL import Image

TOKEN = '*********************************************'

sotrudnik_image = Image.open('сотрудник.png')
sotrudnik_wasted_image = Image.open('сотрудник_потрачено.png')
burokrat_image = Image.open('бюрократ.png')
burokrat_wasted_image = Image.open('бюрократ_потрачено.png')
rieltor_image = Image.open('риелтор.png')
rieltor_wasted_image = Image.open('риелтор_потрачено.png')
gyrnalist_image = Image.open('журналист.png')
gyrnalist_wasted_image = Image.open('журналист_потрачено.png')
notarius_image = Image.open('нотариус.png')
notarius_wasted_image = Image.open('нотариус_потрачено.png')

pribil_image = Image.open('прибыль.png')
resursi_image = Image.open('ресурсы.png')
vzyatka_image = Image.open('взятка.png')
obman_image = Image.open('обман.png')
pluralizm_image = Image.open('плюрализм.png')
zaveshane_image = Image.open('завещание.png')
perestroika_image = Image.open('перестройка.png')
action_images = {'прибыль': pribil_image, 'ресурсы': resursi_image, 'взятка': vzyatka_image, 'обман': obman_image, 'плюрализм': pluralizm_image, 'завещание': zaveshane_image, 'перестройка': perestroika_image}
win_image = Image.open('победа.png')

CARDS = [
         {'id': 1, 'image': sotrudnik_image, 'wasted_image': sotrudnik_wasted_image, 'name': 'Сотрудник ОБХСС', 'action':'ресурсы', 'description': 'Ресурсы. \nВозьмите 1 монету из бюджета. Совершите дополнительное действие. Нельзя использовать эту карту 2 раза в течение одного хода.'}, 
         {'id': 2, 'image': burokrat_image, 'wasted_image': burokrat_wasted_image, 'name': 'Бюрократ', 'action':'взятка', 'description': 'Взятка. \nВозьмите 2 монеты у другого игрока.'},
         {'id': 3, 'image': rieltor_image, 'wasted_image': rieltor_wasted_image, 'name': 'Риелтор', 'action':'обман', 'description': 'Обман. \nЗаплатите 3 монеты другому игроку и устраните его персонажа.'},
         {'id': 4, 'image': gyrnalist_image, 'wasted_image': gyrnalist_wasted_image, 'name': 'Журналист', 'action':'плюрализм', 'description': 'Плюрализм мнений. \nОбменяйте 2 карты.'},
         {'id': 5, 'image': notarius_image, 'wasted_image': notarius_wasted_image, 'name': 'Нотариус', 'action':'завещание', 'description': 'Завещание. \nВозьмите все монеты у выбывшего игрока.'}
         ]

