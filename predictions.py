﻿from datetime import datetime, timedelta
import random

from data import user_data_manager as udm

TOTAL_QUESTION_NUM = 4
			
# Генерация гороскопа (упрощенная версия)
def generate_prediction(user_data) -> str:
	# Прогнозы для знаков
	increment = user_data[udm.INCREMENT]
	zodiac_sign = get_zodiac_sign(user_data[udm.BIRTHDATE_KEY])
	zodiac_prediction = zodiac_predictions[zodiac_index[zodiac_sign] + increment]
	
	# Прогноз на основе проведенного опроса
	personality_prediction = get_personality_prediction(user_data[udm.ANSWER_ORDER], increment)
	
	user_data[udm.LAST_TIME_USED] = datetime.now().strftime('%d.%m.%Y')
	udm.save_user_data(user_data)

	return f"Твой знак зодиака: {zodiac_sign}.\nВот твой гороскоп на сегодня:\n{zodiac_prediction} {personality_prediction}"
		
def get_personality_prediction(answers_order: list[int], increment : int) -> str:
	# Персонализация на основе ответов пользователя
	personality_prediction = ""
	
	for index in answers_order:
		personality_prediction += reply_predictions[(index + increment) % len(reply_predictions)]

	return personality_prediction

# Создает и возвращает случайное предсказание
# user_data нужен для сохранения данных, поскольку эта функция может сгенерировать случайное предсказание и не требует никаких проверок
def get_new_preditction(user_data):
	user_data[udm.INCREMENT] += 1
	udm.save_user_data(user_data)

	prediction = generate_prediction(user_data)
	
	return f"Вот твой гороскоп на сегодня:\n{prediction}"

def get_answer_index(answer: str):
	for key in marks:
		if (key in answer.lower()):
			return marks[key]
	return -1

# ---------------------
# Данные:    
# ---------------------

zodiac_predictions = [
	"Сегодня ты полон энергии и амбиций, но будь осторожен: поспешные решения могут привести к ошибкам.",
	"Твоя решимость поможет тебе преодолеть любые преграды, но не забывай о поддержке близких.",
	"Попробуй направить свою энергию на долгосрочные проекты, это принесет хорошие результаты.",
	"Избегай конфликтов, особенно на работе — сегодня лучше следовать проверенным решениям.",
	"Найди время для саморефлексии, чтобы лучше понять свои истинные желания.",
	"Сегодняшний день принесет возможность начать что-то новое, будь готов к переменам.",
	"День будет удачным для финансовых дел. Но не забывай отдыхать, чтобы сохранить баланс.",
	"Сконцентрируйся на планировании, это поможет тебе избежать неожиданных препятствий.",
	"Сегодня возможны неожиданные финансовые поступления, будь готов к приятным сюрпризам.",
	"Будь осторожен с крупными покупками — лучше тщательно взвесить все решения.",
	"Окружающие могут нуждаться в твоей поддержке, не отказывайся помочь.",
	"Твоя настойчивость сегодня поможет тебе достичь поставленных целей.",
	"Тебя ждёт день, полный общения и новых возможностей. Не упускай шанс научиться чему-то новому.",
	"Лёгкость на подъём сегодня поможет тебе наладить новые связи и узнать что-то важное.",
	"Поддерживай разговоры с теми, кто может помочь в будущем – это откроет перед тобой новые двери.",
	"Тебе стоит внимательно относиться к своим словам, чтобы избежать недоразумений.",
	"Сегодня возможны неожиданные встречи, которые могут повлиять на будущее.",
	"Твоя гибкость и умение приспосабливаться помогут тебе избежать стрессовых ситуаций.",
	"Сегодня лучше сосредоточиться на личных делах и семейных отношениях. Эмоции могут играть важную роль.",
	"Не бойся погрузиться в свои чувства, они подскажут верные решения в сложных ситуациях.",
	"Твоя забота о близких будет высоко оценена, не упускай возможности укрепить семейные узы.",
	"Старайся сохранять эмоциональный баланс, чтобы не перегружать себя и окружающих.",
	"Сегодняшний день отлично подходит для работы над собой и внутренним ростом.",
	"Слушай свою интуицию — она поможет найти верный путь в сложной ситуации.",
	"День подходит для того, чтобы быть в центре внимания. Используй свои лидерские качества с умом.",
	"Проявляй уверенность, но избегай чрезмерной гордости – это поможет тебе наладить контакты с окружающими.",
	"Сегодня идеальный день для презентации своих идей или проектов, будь смелее.",
	"Сегодня будь готов к тому, что окружающие будут ждать от тебя решения — не подведи.",
	"Проявляй щедрость, и она вернётся к тебе в двойном размере.",
	"Не забывай заботиться о своём здоровье, даже когда весь мир в твоих руках.",
	"Организованность и внимание к деталям помогут тебе справиться с любой задачей. Не упускай мелочей.",
	"Сегодня твои аналитические способности помогут решить сложные проблемы.",
	"Не бойся брать на себя дополнительные обязанности, это принесет новые возможности для роста.",
	"Избегай чрезмерного перфекционизма — иногда достаточно просто хорошего результата.",
	"Твоя забота о здоровье сегодня особенно важна, удели внимание профилактике.",
	"Сегодня можно навести порядок не только в делах, но и в мыслях — это принесёт ясность.",
	"Тебя ждёт гармоничный день, если сможешь найти баланс между личной жизнью и работой.",
	"Сегодня важно следить за своим внутренним равновесием, чтобы избежать ненужных конфликтов.",
	"Ищите компромиссы – это будет ключом к успеху во всех аспектах твоей жизни.",
	"Сегодня твоя способность слушать и понимать других поможет избежать сложных ситуаций.",
	"Будь внимателен к своему окружению — возможно, кто-то нуждается в твоей поддержке.",
	"Не торопись с решением важных вопросов — гармония придёт через терпение.",
	"День может принести неожиданные события. Сохраняй хладнокровие и используй свою интуицию.",
	"Не бойся рисковать, но помни о мере – интуиция поможет выбрать правильный путь.",
	"Будь готов к неожиданностям – возможно, именно они принесут наибольшие возможности.",
	"Сегодня удача будет на твоей стороне, если ты доверишься своим инстинктам.",
	"Сохраняй спокойствие, даже если события будут разворачиваться не по твоему сценарию.",
	"Ожидай важной новости — она может оказать значительное влияние на твои планы.",
	"Твои мечты и планы могут начать осуществляться. Однако будь готов адаптироваться к изменениям.",
	"Сегодня возможны приятные сюрпризы и успех в делах, которые давно откладывались.",
	"Поддерживай оптимизм, даже если планы меняются – в этом может быть скрыта удача.",
	"Сегодня отличный день для начала чего-то нового, будь открыт к новым возможностям.",
	"Не бойся рисковать — иногда перемены открывают новые горизонты.",
	"Будь гибким в своих ожиданиях, это позволит легче справляться с изменениями.",
	"Твой труд и усердие сегодня принесут плоды. Главное — не забывать отдыхать и находить время для себя.",
	"День благоприятен для продвижения карьеры, но не забывай о важности личного времени.",
	"Придерживайся своего плана, и твои усилия вскоре будут вознаграждены.",
	"Не забывай делегировать задачи — это поможет тебе сохранить силы для важных дел.",
	"Сконцентрируйся на долгосрочных целях, они принесут наибольшую выгоду.",
	"Сегодня важен баланс между работой и отдыхом — удели время своим хобби.",
	"Сегодня день для креативных идей и общения с единомышленниками. Возможно, перед тобой откроются новые перспективы.",
	"Сегодня важно проявить креативность и не бояться выходить за рамки привычного.",
	"Взаимодействие с новыми людьми может открыть перед тобой необычные перспективы.",
	"Будь готов к неожиданным предложениям, которые могут кардинально изменить твои планы.",
	"Сегодня удачный день для творчества — не бойся выражать свои идеи.",
	"Твоя независимость поможет тебе найти необычные решения для привычных задач.",
	"Сегодня лучше уделить время себе и своим чувствам. Медитация или творчество помогут восстановить силы.",
	"Творческая деятельность поможет снять стресс и откроет новые идеи для будущих проектов.",
	"Не бойся погружаться в свои мечты, это время для внутренней гармонии и восстановления.",
	"Сегодня интуиция подскажет тебе верные решения, если прислушаешься к своим чувствам.",
	"Не торопись с выводами — иногда важно дать событиям развиваться естественно.",
	"Откройтесь духовной практике или медитации, это поможет восстановить внутренний баланс."
]

zodiac_index = {
	"Овен": 0,
	"Телец": 6,
	"Близнецы": 12,
	"Рак": 18,
	"Лев": 24,
	"Дева": 30,
	"Весы": 36,
	"Скорпион": 42,
	"Стрелец": 48,
	"Козерог": 54,
	"Водолей": 60,
	"Рыбы": 66
}	

# Получить знак зодиака
def get_zodiac_sign(birthdate_str: str) -> str:
	
	birthdate = datetime.strptime(birthdate_str, '%d.%m.%Y')
	day = birthdate.day
	month = birthdate.month
	
	if (month == 12 and day >= 22) or (month == 1 and day <= 19):
		return "Козерог"
	elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
		return "Водолей"
	elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
		return "Рыбы"
	elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
		return "Овен"
	elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
		return "Телец"
	elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
		return "Близнецы"
	elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
		return "Рак"
	elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
		return "Лев"
	elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
		return "Дева"
	elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
		return "Весы"
	elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
		return "Скорпион"
	elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
		return "Стрелец"
	
	return ""

marks = {
    'спокойств': 0,
    'паник': 1,
    'анализ': 2,
    'принима': 3,
    'игнор': 4,
    'обиж': 5,
    'успех': 6,
    'комфорт': 7,
    'признани': 8,
    'прям': 9,
    'тактич': 10,
    'уклон': 11,
    'энтузиазм': 12,
    'опаск': 13,
    'равнодуш': 14,
    'достижен': 15,
    'поддерж': 16,
    'совершенств': 17,
    'всегд': 18,
    'иногда': 19,
    'никогд': 20,
    'рост': 21,
    'угроз': 22,
    'нейтрал': 23,
    'согласи': 24,
    'творчеств': 25,
    'результат': 26,
    'интуи': 27,
    'логик': 28,
    'опыт': 29
}


questions = [
	"Как ты справляешься со стрессом: сохраняешь спокойствие, паникуешь или анализируешь ситуацию?",
	"Как ты реагируешь на критику: принимаешь её, игнорируешь или обижаешься?",
	"Что для тебя важнее: успех, комфорт или признание?",
	"Какой стиль общения предпочитаешь: прямой, тактичный или уклончивый?",
	"Как ты относишься к переменам: с энтузиазмом, с опаской или с равнодушием?",
	"Что тебя мотивирует: достижения, поддержка друзей или самосовершенствование?",
	"Как часто ты берешь инициативу в свои руки: всегда, иногда или никогда?",
	"Как ты воспринимаешь критику: как возможность для роста, как угрозу или нейтрально?",
	"Что важнее для тебя в команде: согласие, творчество или результат?",
	"Как ты принимаешь решения: интуитивно, логически или опираясь на опыт?"
]

reply_predictions = [
    "Скоро ты поймёшь, что многое зависит от твоих действий.",
    "Не стоит бояться перемен, они могут принести хорошие результаты.",
    "Важно не торопиться с выводами, особенно в трудных ситуациях.",
    "Тебе следует помнить, что иногда стоит просто ждать.",
    "В ближайшее время ты увидишь, как всё постепенно налаживается.",
    "Не забывай, что каждый шаг имеет значение, даже если он мал.",
    "Постепенно ты начнёшь осознавать свои настоящие желания.",
    "Важно сохранять терпение в моменты неопределённости.",
    "Не упускай возможности учиться на своих ошибках.",
    "Скоро ты обнаружишь, что все трудности временные.",
    "Смело принимай решения, даже если они кажутся сложными.",
    "Помни, что поддержка друзей может сыграть важную роль.",
    "Каждый новый опыт — это возможность для роста.",
    "Не бойся высказывать свои мысли и чувства.",
    "Твои усилия со временем принесут свои плоды.",
    "Важно уметь видеть позитив в сложных ситуациях.",
    "Скоро ты найдёшь ответ на свой давний вопрос.",
    "Не торопись с выводами, дай себе время на размышления.",
    "Слушай свою интуицию, она может направить тебя.",
    "Принимая решения, учитывай свои внутренние ощущения.",
    "Будь открытым к новым идеям и мнениям.",
    "Успех приходит к тем, кто не боится пробовать новое.",
    "Скоро ты ощутишь облегчение и уверенность в своих действиях.",
    "Каждый день приносит новые возможности и надежды.",
    "Важно следовать своим целям, несмотря на преграды.",
    "Не забывай, что даже малые шаги важны.",
    "Скоро ты поймёшь, что все трудности преодолимы.",
    "Принимай изменения как часть своего пути.",
    "Открытость к переменам может изменить твою жизнь к лучшему.",
    "Каждый новый день — это шанс начать что-то новое.",
    "Помни, что позитивный настрой помогает преодолевать преграды.",
    "Не бойся спрашивать и искать помощь, когда это нужно."
]

