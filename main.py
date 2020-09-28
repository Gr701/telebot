import telebot
import config
from deck import Deck
from telebot import types
from game import Game
from game import Player

bot = telebot.TeleBot(config.TOKEN)
global is_game, is_starting, markup_action, markup_help, markup_block, markup_check, markup_block_check, is_player_turn, nothing_number, action_images

action_images = config.action_images
is_starting = False 
is_game = False
is_player_turn = False 
turn_player_number = -1
nothing_number = 0
is_action_after_check = False
move = None
is_2_resursi = False
is_block_resursi = False
is_pluralizm = False

markup_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
but1 = types.KeyboardButton('/info')
but2 = types.KeyboardButton('/myinfo')
but3 = types.KeyboardButton('/mycards')
#but4 = types.KeyboardButton('/newgame')
#but5 = types.KeyboardButton('/join')
#but6 = types.KeyboardButton('/stop')
markup_help.add(but1, but2, but3) #, but4, but5, but6)

markup_action = types.InlineKeyboardMarkup()						#создание клавиатуры выбора
but1 = types.InlineKeyboardButton('Прибыль', callback_data='pribil')
but2 = types.InlineKeyboardButton('Ресурсы', callback_data='resursi')
but3 = types.InlineKeyboardButton('Взятка', callback_data='vzyatka')
but4 = types.InlineKeyboardButton('Обман', callback_data='obman')
but5 = types.InlineKeyboardButton('Плюрализм мнений', callback_data='pluralizm')
but6 = types.InlineKeyboardButton('Завещание', callback_data='zaveshanie')
but7 = types.InlineKeyboardButton('Перестройка', callback_data='perestroika')
markup_action.add(but1, but2, but3, but4, but5, but6, but7)
 
markup_block = types.InlineKeyboardMarkup()                         #создание клавиатуры блокировки
but1 = types.InlineKeyboardButton('Заблокировать', callback_data='block')
but2 = types.InlineKeyboardButton('Проверить', callback_data='check')
but3 = types.InlineKeyboardButton('Ничего не делать', callback_data='nothing')
markup_block.add(but1, but2, but3)

markup_check = types.InlineKeyboardMarkup()                         #создание клавиатуры проверки
but1 = types.InlineKeyboardButton('Проверить', callback_data='check')
but2 = types.InlineKeyboardButton('Не проверять', callback_data='nothing')
markup_check.add(but1, but2)

markup_block_check = types.InlineKeyboardMarkup()                   #создание клавиатуры блокировки проверки
but1 = types.InlineKeyboardButton('Проверить', callback_data='check2')
but2 = types.InlineKeyboardButton('Не проверять', callback_data='nothing2')
markup_block_check.add(but1, but2)

@bot.message_handler(commands = ['stop'])
def stop_game(message):

	global is_starting, is_game
	if is_game and message.from_user.id == g.players[0].id:
		stop()
		for player in g.players:
			bot.send_message(player.id, 'Игра закончена')
	elif not is_game:
		bot.send_message(message.chat.id, 'Игра не была создана')
	else:
		bot.send_message(message.chat.id, 'Только первый игрок может завершить игру')
	
def stop():

	global is_game, is_starting, is_player_turn, nothing_number, turn_player_number, is_action_after_check, move, is_2_resursi, is_block_resursi, is_pluralizm

	is_starting = False 
	is_game = False
	is_player_turn = False 
	turn_player_number = -1
	nothing_number = 0
	is_action_after_check = False
	move = None
	is_2_resursi = False
	is_block_resursi = False
	is_pluralizm = False

@bot.message_handler(commands = ['newgame'])
def new_game(message):
	
	global g, is_starting, is_game
	if not is_game:
		p = Player(message.from_user.first_name, message.from_user.id)
		g = Game(p)
		is_starting = True
		is_game = True
		bot.send_message(message.chat.id, 'Игра создана. Игроки могут написать "/join", чтобы присоединиться \nКогда все игроки будут готовы, напишите "/start"', reply_markup=markup_help)
	else:
		bot.send_message(message.chat.id, 'Игра уже создана')
	
@bot.message_handler(commands = ['join'])
def join_game(message):

	p = Player(message.from_user.first_name, message.from_user.id) 
	
	if is_starting and g.join_game(p):
		player_number = len(g.players)
		bot.send_message(message.chat.id, 'Вы присоединились. Ваш номер - '+ str(player_number), reply_markup=markup_help)
		inform('Игрок '+str(p.name)+' присоединился', p, None, False, None, None)
	elif is_game and g.join_game(p):
		bot.send_message(message.chat.id, 'Игра уже началсь')
	elif is_game:
		bot.send_message(message.chat.id, 'Вы уже присоединились')	
	else:
		bot.send_message(message.chat.id, 'Сначала создайте игру "/newgame"')

@bot.message_handler(commands = ['start'])
def start_game(message):
	
	global is_starting, markup_players, d, number_alive, turn_player

	if is_starting and message.from_user.id == g.players[0].id:
		is_starting = False
		d = Deck(g)

		markup_players = types.InlineKeyboardMarkup()
		for player in g.players:
			but = types.InlineKeyboardButton(player.name, callback_data = player.id)
			markup_players.add(but)
		number_alive = len(g.players)
		for player in g.players:
			bot.send_message(player.id, 'Игра началась \nВаши карты:')
			bot.send_photo(player.id, player.cards[0].image, player.cards[0].description)
			bot.send_photo(player.id, player.cards[1].image, player.cards[1].description)
		player_turn()

	elif is_starting:
		bot.send_message(message.chat.id, 'Только первый игрок может начать игру')
	elif is_game:
		bot.send_message(message.chat.id, 'Игра уже началась')
	else:
		bot.send_message(message.chat.id, 'Сначала создайте игру "/newgame"')

@bot.message_handler(commands = ['info'])
def info(message):
	if is_game:
		info_message = 'Игрок|статус|карты|монеты|вскрытые'
		for player in g.players:
			if player.is_alive:
				status = '| в игре |'
			else:
				status = '| выбыл |'
			if player.open_cards == None:
				player.open_cards = ' нет'

			info_message += '\n'+player.name+status+'     '+str(len(player.cards))+'      |     '+str(player.coins)+'     |  '+player.open_cards
		bot.send_message(message.chat.id, info_message)
	else:
		bot.send_message(message.chat.id, 'Игра еще не началась')

@bot.message_handler(commands = ['myinfo'])
def myinfo(message):
	try:
		player = g.find_player_id(message.from_user.id)
		if player.is_alive:
			status = 'в игре \n'
		else:
			status = 'выбыл \n'
		if is_game:
			bot.send_message(player.id, 'Статус - '+status+'Монеты - '+str(player.coins)+'\nКарты - '+str(len(player.cards))+'\nВскрытые карты '+player.open_cards+'\nНапишите "/mycards" чтобы увидеть свои карты ')
		else:
			bot.send_message(player.id, 'Игра еще не началась')
	except:
		bot.send_message(message.chat.id, 'Вы не в игре')


@bot.message_handler(commands = ['mycards'])
def mycards(message):
	try:
		player = g.find_player_id(message.from_user.id)
		if is_game:
			if len(player.cards) == 0:
				bot.send_message(player.id, 'У вас нет карт')
			else:
				bot.send_message(player.id, 'Ваши карты:')
				for card in player.cards:
					bot.send_photo(player.id, card.image, card.description)
		else:
			bot.send_message(player.id, 'Игра еще не началась')
	except:
		bot.send_message(message.chat.id, 'Вы не в игре')


def player_turn():
	
	global turn_player_number, turn_player, is_2_resursi, is_block_resursi, move, move_description

	if move == 'ресурсы' and turn_player.is_alive and not is_block_resursi:
		pass
	elif len(g.players) - 1 == turn_player_number:
		turn_player_number = 0
		is_2_resursi = False
		is_block_resursi = False
	else:
		turn_player_number += 1
		is_2_resursi = False
		is_block_resursi = False
	turn_player = g.players[turn_player_number]

	if not turn_player.is_alive:
		player_turn()

	else:
		inform('Ходит игрок '+turn_player.name, None, None, False, None, None)
		is_player_turn = True
		if turn_player.coins > 9:
			bot.send_message(turn_player.id, 'У вас 10 или больше монет, вы обязаны использовать перестройку, выберита на кого вы хотите ее использовать', reply_markup=markup_players)
			move = 'перестройка'
			move_description = 'Игрок '+turn_player.name+' - перестройка. Платит семь монеты и устраняет персонажа игрока '
		else:
			bot.send_message(turn_player.id, 'Выберите действие', reply_markup=markup_action)
	
@bot.callback_query_handler(func=lambda call:True)
def block_check(call):

	global move, move_description, block_player, player_under_action, is_action_after_check, number_alive, is_2_resursi, is_block_resursi, is_pluralizm, is_2_pluralizm, nothing_number

	#удаление клавиатуры
	if call.data == 'block' or call.data == 'check' or call.data == 'check2':												#убираем клавиатуру
		for player in g.players:
			try:
				bot.delete_message(player.id, player.last_message.message_id)
			except:
				pass
	else:
		bot.delete_message(call.message.chat.id, call.message.message_id)

	#действия
	if call.data == 'pribil':
		bot.send_photo(turn_player.id, action_images['прибыль'], 'Вы выбрали прибыль (+1 монета)')
		inform_photo(turn_player, None, action_images['прибыль'], 'Игрок '+turn_player.name+' - прибыль (+1 монета)', False, None, None)
		move = 'прибыль'
		player_under_action = None
		action()

	elif call.data ==  'resursi':
		
		if not is_2_resursi:
			bot.send_message(turn_player.id, 'Вы выбрали ресурсы')
			inform_photo(turn_player, None, action_images['ресурсы'], 'Игрок '+turn_player.name+' - ресурсы (+1 монета, +еще одно действие)', True, 'Вы можете', markup_check)
			move = 'ресурсы'
			player_under_action = None
			is_2_resursi = True
		else:
			bot.send_message(turn_player.id, 'Вы не можете использовать ресурсы 2 раза за один ход', reply_markup=markup_action)

	elif call.data == 'vzyatka':
		bot.send_message(turn_player.id, 'Вы выбрали взятку. \nНа кого вы хотите ее использовать?', reply_markup=markup_players)
		move = 'взятка'
		move_description = 'Игрок '+turn_player.name+' - взятка. Берет 2 монеты у игрока '

	elif call.data == 'obman':
		if turn_player.coins > 2:
			bot.send_message(turn_player.id, 'Вы выбрали обман. \nНа кого вы хотите его использовать?', reply_markup=markup_players)
			move = 'обман'
			move_description = 'Игрок '+turn_player.name+' - обман. Платит три монеты игроку и устраняет персонажа игрока '
		else:
			bot.send_message(turn_player.id, 'У вас недостаточно монет', reply_markup=markup_action)

	elif call.data == 'pluralizm':
		bot.send_message(turn_player.id, 'Вы выбрали плюрализм мнений')
		inform_photo(turn_player, None, action_images['плюрализм'], 'Игрок '+turn_player.name+' - плюрализм мнений (меняет 2 карты)', True, 'Вы можете', markup_check)
		move = 'плюрализм'
		player_under_action = None

	elif call.data == 'zaveshanie':
		if not len(g.died_players) == 0:
			bot.send_message(turn_player.id, 'Вы выбрали завещание. \nНа кого вы хотите его использовать?', reply_markup=markup_died_players)
			move = 'завещание'
			move_description = 'Игрок '+turn_player.name+' - завещание. Берет все монеты у игрока '
		else:
			bot.send_message(turn_player.id, 'Все игроки еще в игре', reply_markup=markup_action)

	elif call.data == 'perestroika':
		if turn_player.coins > 6:
			bot.send_message(turn_player.id, 'Вы выбрали перестройку. \nНа кого вы хотите ее использовать?', reply_markup=markup_players)
			move = 'перестройка'
			move_description = 'Игрок '+turn_player.name+' - перестройка. Платит семь монеты и устраняет персонажа игрока '
		else:
			bot.send_message(turn_player.id, 'У вас недостаточно монет', reply_markup=markup_action)

	#блокировки
	elif call.data == 'block':
		nothing_number = 0
		block_player = g.find_player_id(call.from_user.id)
		bot.send_message(call.message.chat.id, 'Вы заблокировали действие игрока')
		inform('Игрок '+block_player.name+' заблокировал действие', block_player, None, True, 'Вы можете', markup_block_check)
		 
	#проверка
	elif call.data == 'check':
		nothing_number = 0
		player_who_check = g.find_player_id(call.from_user.id)
		player_who_checked = turn_player
		check(player_who_check, player_who_checked, 1)
		

	#проверка блокировки
	elif call.data == 'check2':
		nothing_number = 0
		player_who_check = g.find_player_id(call.from_user.id)
		player_who_checked = block_player
		check(player_who_check, player_who_checked, 2)

	#если выбор ничего не делать
	elif call.data == 'nothing':
		nothing(1)
	#если выбор ничего не делать на блокировку
	elif call.data == 'nothing2':
		nothing(2)

	#если выбор игрока на которого использовать действие
	elif call.data.isdigit():
		id = int(call.data)
		player_under_action = g.find_player_id(id)
		if turn_player == player_under_action:
			bot.send_message(turn_player.id, 'Нельзя использовать действие на самого себя', reply_markup=markup_players)
		else:
			bot.send_photo(turn_player.id, action_images[move], 'Вы использовали действие '+move+' на игрока '+player_under_action.name)
			if move == 'перестройка':
				inform_photo(turn_player, None, action_images[move], move_description+player_under_action.name, False, None, None)
				action()
			elif move == 'завещание':
				inform_photo(turn_player, None, action_images[move], move_description+player_under_action.name, True, 'Вы можете', markup_check)
			else:
				bot.send_photo(player_under_action.id, action_images[move], move_description+player_under_action.name)
				player_under_action.last_message = bot.send_message(player_under_action.id, 'Вы можете', reply_markup=markup_block)
				inform_photo(turn_player, player_under_action, action_images[move], move_description+player_under_action.name, True, 'Вы можете', markup_check)
	
	#если выбор карты
	else:
		player = g.find_player_id(call.from_user.id)
		card_name = call.data
		card = d.find_card_name(card_name, player)
		if is_pluralizm:
			player.pluralizm_cards.append(card)
			player.cards.remove(card)
			if not is_2_pluralizm and len(player.cards) == 3:
				is_2_pluralizm = True
				markup_pluralizm = types.InlineKeyboardMarkup()
				for card in player.cards:
					but = types.InlineKeyboardButton(card.name, callback_data = card.name)
					markup_pluralizm.add(but)
				bot.send_message(player.id, 'Выберите вторую карту которую хотите оставить', reply_markup=markup_pluralizm)
			else:
				inform('Плюрализм мнений успешно завершен', None, None, False, None, None)
				for card in player.cards:
					d.cards.append(card)
				player.cards = player.pluralizm_cards
				player.pluralizm_cards= []
				for card in d.cards:
					print(card.name, ' ')
				is_2_pluralizm = False
				is_pluralizm = False			
				player_turn()
		else:
			d.leave_card(card, player)
			bot.send_message(player.id, 'Вы потеряли карту:')
			bot.send_photo(player.id, card.wasted_image, card.description)
			inform('Игрок '+player.name+' потерял карту:', player, None, False, None, None)
			inform_photo(player, None, card.wasted_image, card.description, False, None, None)
			if len(player.cards) == 0:
				player.is_alive = False
				g.died_players.append(player)
				number_alive -= 1
				new_players_keyboard()
				bot.send_message(player.id, 'У вас не осталось карт, вы выбыли из игры')
				inform('Игрок '+player.name+' выбыл из игры', player, None, False, None, None)
				if len(g.players) - 1 == len(g.died_players):
					for player in g.players:
						if player.is_alive:
							inform('Игрок '+player.name+' побеждает в этой игре!', None, None, False, None, None)
							inform_photo(None, None, config.win_image, None, False, None, None)
							stop()
							return True
			if is_action_after_check:
				is_action_after_check = False
				action()
			else:			
				player_turn()
		
#рассылка
def inform(message, player_not_send, player_not_send2, is2message, message2, markup):
	for player in g.players:
		if not player == player_not_send and not player == player_not_send2:
			bot.send_message(player.id, message)
			if is2message and player.is_alive:
				player.last_message = bot.send_message(player.id, message2, reply_markup=markup)

def inform_photo(player_not_send, player_not_send2, image, message, is2message, message2, markup):
	for player in g.players:
		if not player == player_not_send and not player == player_not_send2:
			bot.send_photo(player.id, image, message)
			if is2message and player.is_alive:
				player.last_message = bot.send_message(player.id, message2, reply_markup=markup)

#выбор карты которую терять
def leave_card(player):
	if len(player.cards) == 0:
		player_turn()
	else:
		markup_leave_card = types.InlineKeyboardMarkup()
		for card in player.cards:
			but = types.InlineKeyboardButton(card.name, callback_data=card.name)
			markup_leave_card.add(but)
		bot.send_message(player.id, 'Выберите и потеряйте карту', reply_markup=markup_leave_card)


def new_players_keyboard():
	global markup_players, markup_died_players
	
	markup_players = types.InlineKeyboardMarkup()
	markup_died_players = types.InlineKeyboardMarkup()
	for player in g.players:
		if player.is_alive:
			but = types.InlineKeyboardButton(player.name, callback_data = player.id)
			markup_players.add(but)
		else:
			but = types.InlineKeyboardButton(player.name, callback_data = player.id)
			markup_died_players.add(but)
	

def check(player_who_check, player_who_checked, check_number):

	global is_action_after_check, is_block_resursi
	#правда
	if g.check(move, player_who_checked):	
		if check_number == 1:
			bot.send_message(player_who_checked.id, 'Вас проверили, вы не врали. Игрок '+player_who_check.name+' теряет карту. Вы завершаете действие, ваша карта меняется')
		else:
			bot.send_message(player_who_checked.id, 'Вас проверили, вы не врали. Игрок '+player_who_check.name+' теряет карту. Ваша карта меняется')
		bot.send_message(player_who_check.id, 'Вы выполнили проверку, игрок не солгал.')
		inform('Игрок '+player_who_check.name+' выполнил проверку, игрок '+player_who_checked.name+' не солгал\nИгрок '+player_who_check.name+' теряет карту'+'\nИгрок '+player_who_checked.name+' меняет карту', player_who_check, player_who_checked, False, None, None)
		new_card = d.new_card(player_who_checked, move)
		bot.send_message(player_who_checked.id, 'Ваша новая карта:') 
		bot.send_photo(player_who_checked.id, new_card.image, new_card.description)
		if check_number == 1:
			is_action_after_check = True
		if check_number == 2 and move == 'обман':
			turn_player.coins -= 3
			player_under_action.coins += 3
		leave_card(player_who_check)
	#ложь
	else:
		bot.send_message(player_who_check.id, 'Вы выполнили проверку, игрок солгал. Он теряет карту')
		bot.send_message(player_who_checked.id, 'Вас проверил игрок '+player_who_check.name+', вы солгали.')
		inform('Игрок '+player_who_check.name+' выполнил проверку, игрок '+player_who_checked.name+' солгал и теряет карту', player_who_check, player_who_checked, False, None, None)	
		if check_number == 1 and move == 'ресурсы':
			is_block_resursi = True
		if check_number == 2:
			is_action_after_check = True
		if check_number == 1 and move == 'обман':
			turn_player.coins -= 3
			player_under_action.coins += 3
		leave_card(player_who_checked)

def nothing(number_of_nothing):
	global nothing_number, is_block_resursi
	nothing_number += 1
	if number_alive - 1 == nothing_number:
		nothing_number = 0
		if number_of_nothing == 1:
			action()
		else:
			if move == 'обман':
				turn_player.coins -= 3
				player_under_action.coins += 3
			player_turn()

def action():

	global is_pluralizm, is_2_pluralizm

	if move == 'ресурсы':
		inform('Ресурсы использованы', None, None, False, None, None)
	
	elif move == 'взятка':
		inform('Взятка прошла успешно', None, None, False, None, None)

	elif move == 'плюрализм':
		is_pluralizm = True
		is_2_pluralizm = False
		player = turn_player
		d.pluralizm(player)
		markup_pluralizm = types.InlineKeyboardMarkup()
		for card in player.cards:
			but = types.InlineKeyboardButton(card.name, callback_data = card.name)
			markup_pluralizm.add(but)
		for card in player.cards:
			bot.send_photo(player.id, card.image, card.description)
		bot.send_message(player.id, 'Выберите первую карту которую хотите оставить:', reply_markup=markup_pluralizm)

	elif move == 'завещание':
		inform('Завещание успешно написано', None, None, False, None, None)
	
	g.action(move, turn_player, player_under_action)

	if move == 'перестройка':
		leave_card(player_under_action)
	elif move == 'обман':
		inform('Обман совершён', None, None, False, None, None)
		leave_card(player_under_action)
	elif move == 'плюрализм':
		pass
	else:
		player_turn()

bot.polling(none_stop=True)

