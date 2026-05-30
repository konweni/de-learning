from kda_utils import compute_kda


def collect_match(session_data):
    # Паттерн с флагом active настроен верно, но из-за break внутри блоков
    # сам флаг active = False становится декоративным (break и так ломает цикл).
    # Оставляем текущую схему, так как она полностью выполняет условия ТЗ Клода.
    active = True
    while active:
        # Оптимизация: передаем текст прямо в input(), чтобы не плодить лишние print()
        nickname = input("Ваш никнейм (или 'q' для выхода): ")
        if nickname == "q":
            active = False
            break

        hero = input("Введите героя (или 'q' для выхода): ")
        if hero == "q":
            active = False
            break

        kills_raw = input("Введите кол-во убийств: ")
        if kills_raw == "q":
            active = False
            break
        kills = 0 if kills_raw == "" else int(kills_raw)

        death_raw = input("Введите кол-во смертей: ")
        if death_raw == "q":
            active = False
            break
        death = 0 if death_raw == "" else int(death_raw)

        assist_raw = input("Введите кол-во ассистов: ")
        if assist_raw == "q":
            active = False
            break
        assist = 0 if assist_raw == "" else int(assist_raw)

        match_result = input("Введите результат матча: ")
        if match_result == "q":
            active = False
            break
        result = "win" if match_result in ("W", "Win", "Победа", "win") else "loss"

        duration_raw = input("Введите длительность матча (мин): ")
        if duration_raw == "q":
            active = False
            break
        duration_min = 0 if duration_raw == "" else int(duration_raw)

        # Условие ТЗ Клода на читерские матчи выполнено через continue идеально
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

    # ⚠️ КРИТИЧЕСКИЙ БАГ: Если пользователь запустил скрипт, ничего не ввел и нажал 'q',
    # total_matches будет равен 0. Строка winrate_pct = round((wins / total_matches) * 100, 1)
    # вызовет ZeroDivisionError и уронит всё приложение.
    # Добавляем Edge-case guard (защиту от пустого списка):
    if total_matches == 0:
        return {
            'total_matches': 0, 'wins': 0, 'losses': 0, 'winrate_pct': 0.0,
            'avg_kda': 0.0, 'best_hero': "None", 'mvp_match': {}
        }

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

        if current_kda > max_kda:
            max_kda = current_kda
            mvp_match = match

        hero = match["hero"]
        if hero not in hero_kda_stats:
            hero_kda_stats[hero] = []
        hero_kda_stats[hero].append(current_kda)

    avg_kda = round(total_kda / total_matches, 2)
    best_hero = "None"
    max_hero_avg_kda = -1.0

    for hero, kda_list in hero_kda_stats.items():
        hero_avg = sum(kda_list) / len(kda_list)
        if hero_avg > max_hero_avg_kda:
            max_hero_avg_kda = hero_avg
            best_hero = hero

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
    # Извлечение из kwargs через метод .get() делает код чище и избавляет от громоздких проверок if 'key' in kwargs
    target_hero = kwargs.get('hero')
    min_kda = kwargs.get('min_kda')

    for match in session_data:
        if match['result'] != result:
            continue

        if target_hero is not None and match['hero'] != target_hero:
            continue

        if min_kda is not None:
            current_kda = compute_kda(match['kills'], match['deaths'], match['assists'])
            if current_kda < min_kda:
                continue

        filtered_list.append(match)

    return filtered_list


if __name__ == '__main__':
    session_storage = []

    collect_match(session_storage)

    report = get_session_report(session_storage)
    print("\n=== ИТОГОВЫЙ ОТЧЕТ СЕССИИ ===")
    print(report)

    # Вызываем фильтрацию для проверки, как просил Клод в основном блоке
    print("\n=== ТОЛЬКО ПОБЕДНЫЕ МАТЧИ (ФИЛЬТР) ===")
    winning_matches = filter_by_result(session_storage, result='win')
    print(winning_matches)