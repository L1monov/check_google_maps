import json

import pymysql
from config import HOST, PASSWORD, DB,USER
# данные от БД



def get_rewiews_for_check():
    # устанавливаем соединение
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()

    # выполняем следующий запрос
    # cursor.execute(
    #     f"SELECT id, recall FROM u1380978_database.t_request WHERE status = 'Переписывание';"
    # )
    cursor.execute(
        f"""SELECT iga.id_acc_gmail, tr.id, ta.url, tr.recall FROM u1380978_database.info_google_accs iga
                join t_request tr on tr.id = iga.id_review
                join t_area ta on tr.area_id = ta.id
                where iga.is_publish = 'На модерации'  and (iga.date_check != curdate() or iga.date_check is null)"""
    )
    result_set = cursor.fetchall()
    dict_reviews = {}
    count = 0
    for _ in range(len(result_set)):
        dict_reviews[count] ={
            'id_google_acc':result_set[_][0],
            'id_review':result_set[_][1],
            'url': result_set[_][2],
            'recall':result_set[_][3]
        }
        count += 1
    # with open('result.json', 'w', encoding='utf-8') as file:
    #     json.dump(dict_reviews, file, ensure_ascii=False, indent=4)
    conn.close()
    return dict_reviews

def set_status_proverka(dict_for_update):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()
    # выполняем следующий запрос
    # cursor.execute(
    #     f"SELECT id, recall FROM u1380978_database.t_request WHERE status = 'Переписывание';"
    # )
    cursor.execute(
        f"""update u1380978_database.info_google_accs set `is_publish` = 'Проверяется' , `date_check` = curdate()
            where id_acc_gmail = '{dict_for_update['id_google_acc']}'"""
    )
    cursor.execute(f"""
            update u1380978_database.t_request set
            status = 'Проверяется'
            where id = {dict_for_update['id_review']}""")

    conn.commit()
    conn.close()

def set_status_gotovo(dict_for_update):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()
    cursor.execute(
        f"""update u1380978_database.info_google_accs set `is_publish` = 'Готово' , `date_check` = curdate()
            where id_acc_gmail = '{dict_for_update['id_google_acc']}'"""
    )
    cursor.execute(f"""
            update u1380978_database.t_request set
            status = 'Готово'
            where id = {dict_for_update['id_review']}""")

    conn.commit()
    conn.close()

def set_new_slet(dict_for_update):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""update u1380978_database.info_google_accs set `date_check` = curdate(), is_publish = 'Слёт'
            where id_acc_gmail = '{dict_for_update['id_google_acc']}'"""
    )

    conn.commit()
    conn.close()

def set_new_date(dict_for_update):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()
    # выполняем следующий запрос
    # cursor.execute(
    #     f"SELECT id, recall FROM u1380978_database.t_request WHERE status = 'Переписывание';"
    # )
    cursor.execute(
        f"""update u1380978_database.info_google_accs set `date_check` = curdate()
            where id_acc_gmail = '{dict_for_update['id_google_acc']}'"""
    )

    conn.commit()
    conn.close()

def set_new_recall(recall, id_review, rewrite):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()
    cursor.execute(
            f"""update u1380978_database.t_request set `recall` = '{recall}', prim = CONCAT(prim, '\nrewrite {rewrite}'),status = 'В работе', date_doc = curdate()
                where id = '{id_review}'"""
        )
    conn.commit()
    cursor.execute(
            f"""update u1380978_database.info_google_accs set `is_publish` = 'Переписан'
                where id_review = '{id_review}'"""
        )
    conn.commit()
    conn.close()

def get_recalls_for_rewrite():
    # устанавливаем соединение
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""SELECT 
                iga.id_acc_gmail, tr.id, ta.url, tr.recall
            FROM
                u1380978_database.info_google_accs iga
                    JOIN
                t_request tr ON tr.id = iga.id_review
                    JOIN
                t_area ta ON tr.area_id = ta.id
            WHERE
                iga.is_publish = 'На модерации'"""
    )
    result_set = cursor.fetchall()
    dict_reviews = {}
    count = 0
    for _ in range(len(result_set)):
        dict_reviews[count] ={
            'id_google_acc':result_set[_][0],
            'id_review':result_set[_][1],
            'url': result_set[_][2],
            'recall':result_set[_][3]
        }
        count += 1
    conn.close()
    return dict_reviews

def recheck():
    # устанавливаем соединение
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()

    # выполняем следующий запрос
    # cursor.execute(
    #     f"SELECT id, recall FROM u1380978_database.t_request WHERE status = 'Переписывание';"
    # )
    cursor.execute(
        f"""SELECT iga.id_acc_gmail, tr.id, ta.url, tr.recall FROM u1380978_database.info_google_accs iga
                    join t_request tr on tr.id = iga.id_review
                    join t_area ta on tr.area_id = ta.id
                    where iga.is_publish = 'Проверяется'  and date_publish < CURDATE() - INTERVAL 3 DAY"""
    )
    result_set = cursor.fetchall()
    dict_reviews = {}
    count = 0
    for _ in range(len(result_set)):
        dict_reviews[count] = {
            'id_google_acc': result_set[_][0],
            'id_review': result_set[_][1],
            'url': result_set[_][2],
            'recall': result_set[_][3]
        }
        count += 1
    # with open('result.json', 'w', encoding='utf-8') as file:
    #     json.dump(dict_reviews, file, ensure_ascii=False, indent=4)
    conn.close()
    return dict_reviews


