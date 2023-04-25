import telebot
import psycopg2

bot = telebot.TeleBot('6040534547:AAHZmcgbijN7R1hMnWsb-aAHXc2fjnzGSug')


conn = psycopg2.connect(dbname='postgres', user='postgres', password='*******', host='localhost')
cursor = conn.cursor()


def params_preparation(params):
    result_params = []
    for param in params:
        if param.lower() == 'домен':
            result_params.append('domain')
        elif param.lower() == 'функциональная группа':
            result_params.append('functional_group')
        elif param.lower() == 'технология':
            result_params.append('technology')
        elif param.lower() == 'метод использования':
            result_params.append('usage_method')
        elif param.lower() == 'наименование сценария':
            result_params.append('scenario_name')
    return result_params


def search_preparation(result_msg):
    result_params = params_preparation(result_msg[0].replace(', ', ',').split(','))
    if 'usage_method' in result_params:
        return search_with_usage_method(result_params, result_msg)
    elif 'technology' in result_params:
        return search_with_technology(result_params, result_msg)
    elif 'domain' in result_params:
        return search_with_domain(result_params, result_msg)
    elif 'functional_group' in result_params:
        return search_with_func_group(result_params, result_msg)
    elif 'scenario_name' in result_params:
        return search_with_scenario_name(result_params, result_msg)
    else:
        return 0


def search_with_usage_method(result_params, result_msg):
    usage_values = result_msg[result_params.index('usage_method') + 1].split(',')
    sql = 'SELECT * from scenario WHERE dom_id in (SELECT domain_id FROM technology WHERE id in (SELECT tech_id FROM usage_method WHERE name in ('
    for value in usage_values:
        sql += ("\'" + value.lower().strip() + '\', ')
    sql = sql[:-2] + ')))'
    if 'functional_group' in result_params:
        sql += 'and func_id in (SELECT func_id FROM functional_group WHERE name IN ('
        func_values = result_msg[result_params.index('functional_group') + 1].split(',')
        for value in func_values:
            sql += ("\'" + value.lower().strip() + '\', ')
        sql = sql[:-2] + '))'
    if 'scenario_name' in result_params:
        sql += ' and name in ('
        scenario_values = result_msg[result_params.index('scenario_name') + 1].split(',')
        for value in scenario_values:
            sql += ("\'" + value.lower().strip() + '\', ')
        sql = sql[:-2] + ')'
    sql += ';'
    cursor.execute(sql)
    records = cursor.fetchall()
    return records


def search_with_technology(result_params, result_msg):
    result_values = result_msg[result_params.index('technology') + 1].split(',')
    sql = 'SELECT * from scenario WHERE dom_id in (SELECT domain_id FROM technology WHERE name in ('
    for value in result_values:
        sql += ("\'" + value.lower().strip() + '\', ')
    sql = sql[:-2] + '))'
    if 'functional_group' in result_params:
        sql += 'and func_id in (SELECT func_id FROM functional_group WHERE name IN ('
        func_values = result_msg[result_params.index('functional_group') + 1].split(',')
        for value in func_values:
            sql += ("\'" + value.lower().strip() + '\', ')
        sql = sql[:-2] + '))'
    if 'scenario_name' in result_params:
        sql += ' and name in ('
        scenario_values = result_msg[result_params.index('scenario_name') + 1].split(',')
        for value in scenario_values:
            sql += ("\'" + value.lower().strip() + '\', ')
        sql = sql[:-2] + ')'
    sql += ';'
    cursor.execute(sql)
    records = cursor.fetchall()
    return records


def search_with_domain(result_params, result_msg):
    result_values = result_msg[result_params.index('domain') + 1].split(',')
    sql = 'SELECT * from scenario WHERE dom_id in (SELECT domain_id FROM domain WHERE name in ('
    for value in result_values:
        sql += ("\'" + value.lower().strip() + '\', ')
    sql = sql[:-2] + '))'
    if 'functional_group' in result_params:
        sql += 'and func_id in (SELECT func_id FROM functional_group WHERE name IN ('
        func_values = result_msg[result_params.index('functional_group') + 1].split(',')
        for value in func_values:
            sql += ("\'" + value.lower().strip() + '\', ')
        sql = sql[:-2] + '))'
    if 'scenario_name' in result_params:
        sql += ' and name in ('
        scenario_values = result_msg[result_params.index('scenario_name') + 1].split(',')
        for value in scenario_values:
            sql += ("\'" + value.lower().strip() + '\', ')
        sql = sql[:-2] + ')'
    sql += ';'
    cursor.execute(sql)
    records = cursor.fetchall()
    return records


def search_with_func_group(result_params, result_msg):
    result_values = result_msg[result_params.index('functional_group') + 1].split(',')
    sql = 'SELECT * from scenario WHERE func_id in (SELECT func_id FROM functional_group WHERE name in ('
    for value in result_values:
        sql += ("\'" + value.lower().strip() + '\', ')
    sql = sql[:-2] + '))'
    if 'scenario_name' in result_params:
        sql += ' and name in ('
        scenario_values = result_msg[result_params.index('scenario_name') + 1].split(',')
        for value in scenario_values:
            sql += ("\'" + value.lower().strip() + '\', ')
        sql = sql[:-2] + ')'
    sql += ';'
    cursor.execute(sql)
    records = cursor.fetchall()
    return records


def search_with_scenario_name(result_params, result_msg):
    result_values = result_msg[result_params.index('scenario_name') + 1].split(',')
    sql = 'SELECT * from scenario WHERE name in ('
    for value in result_values:
        sql += ("\'" + value.lower().strip() + '\', ')
    sql = sql[:-2] + ');'
    print(sql)
    cursor.execute(sql)
    records = cursor.fetchall()
    return records
