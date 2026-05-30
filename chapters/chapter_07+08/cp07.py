from kda_utils import compute_kda


def collect_match(session_data):
    active = True
    while active:
        print("Ваш никнейм")
        nickname = input()
        if nickname == "q":
            active = False
            break
        hero = input()
        if hero == "q":
            active = False
            break
        print("Введите кол-во убийств")
        kills_raw = input()
        if kills_raw == "q":
            active = False
            break
        if kills_raw == "":
            kills = 0
        else:
            kills = int(kills_raw)
        print("Введите кол-во смертей")
        death_raw = input()
        if death_raw == "q":
            active = False
            break
        if death_raw == "":
            death = 0
        else:
            death = int(death_raw)
        print("Введите кол-во ассистов")
        assist_raw = input()
        if assist_raw == "q":
            active = False
            break
        if assist_raw == "":
            assist = 0
        else:
            assist = int(assist_raw)
        print("Введите результат матча")
        match_result = input()
        if match_result == "q":
            active = False
            break
        result = "win" if match_result in ("W", "Win", "Победа", "win") else "loss"
        print("Введите длительность матча (мин)")
        duration_raw = input()
        if duration_raw == "q":
            active = False
            break
        duration_min = 0 if duration_raw == "" else int(duration_raw)
        if duration_min < 5:
            print("Матч слишком короткий (< 5 мин). Пропускаем...")
            continue
        match_record = {
            'player': nickname,
            'hero': hero,
            'kills': kills,
            'deaths': death,
            'assists': assist,
            'result': result,
            'duration_min': duration_min
        }
        session_data.append(match_record)


def get_session_report(session_data):
    data_copy = session_data[:]
    total_matches = len(data_copy)
    wins = 0
    losses = 0
    for match in data_copy:
        if match["result"] == "win":
            wins += 1
        else:
            losses += 1
    winrate_pct = round((wins / total_matches) * 100, 1)
    total_kda = 0.0
    max_kda = -1.0
    mvp_match = {}
    hero_kda_stats = {}
    for match in data_copy:
        current_kda = compute_kda(match["kills"], match["deaths"], match["assists"])
        total_kda += current_kda

        # 1. Проверка на MVP (внутри цикла)
        if current_kda > max_kda:
            max_kda = current_kda
            mvp_match = match

        # 2. Сбор статистики по героям (внутри цикла, но ОТДЕЛЬНО от if выше)
        hero = match["hero"]
        if hero not in hero_kda_stats:
            hero_kda_stats[hero] = []
        hero_kda_stats[hero].append(current_kda)
# 1. Выравниваем отступы (4 пробела от края)
    avg_kda = round(total_kda / total_matches, 2)
    best_hero = "None"
    max_hero_avg_kda = -1.0

    # 2. Перебираем персонажей и списки их KDA
    for hero, kda_list in hero_kda_stats.items():
        hero_avg = sum(kda_list) / len(kda_list)  # Находим среднее для конкретного героя
        if hero_avg > max_hero_avg_kda:
            max_hero_avg_kda = hero_avg
            best_hero = hero

    # 3. Возвращаем готовый словарь с метриками наружу
    return {
        'total_matches': total_matches,
        'wins': wins,
        'losses': losses,
        'winrate_pct': winrate_pct,
        'avg_kda': avg_kda,
        'best_hero': best_hero,
        'mvp_match': mvp_match
    }


def filter_by_result(session_data, result='win', **kwargs):
    filtered_list = []

    for match in session_data:
        # 1. Если результат не совпадает с искомым (win/loss), пропускаем матч
        if match['result'] != result:
            continue

        # 2. Если передали фильтр по герою, и он не совпадает — пропускаем
        if 'hero' in kwargs and kwargs['hero'] is not None:
            if match['hero'] != kwargs['hero']:
                continue

        # 3. Если передали фильтр по минимальному KDA, и он ниже нужного — пропускаем
        if 'min_kda' in kwargs and kwargs['min_kda'] is not None:
            current_kda = compute_kda(match['kills'], match['deaths'], match['assists'])
            if current_kda < kwargs['min_kda']:
                continue

        # Если матч прошел все проверки, добавляем его в наш список
        filtered_list.append(match)

    return filtered_list


if __name__ == '__main__':
    session_storage = []

    # 1. Запускаем сбор матчей через консоль
    collect_match(session_storage)

    # 2. Генерируем и выводим отчет по собранным данным
    report = get_session_report(session_storage)
    print("\n=== ИТОГОВЫЙ ОТЧЕТ СЕССИИ ===")
    print(report)