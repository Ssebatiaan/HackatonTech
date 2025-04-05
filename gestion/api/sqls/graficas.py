from django.db import connection
import pandas as pd
import psycopg2



def get_grafica_query_sql(sql_graficas, condiciones_graficas):
    SQL_GRAFICAS = sql_graficas
    cursor = connection.cursor()
    try:
        if condiciones_graficas:
            SQL_GRAFICAS = SQL_GRAFICAS.format(condiciones_graficas = " AND " + condiciones_graficas)
        else:
            SQL_GRAFICAS = SQL_GRAFICAS.replace("{condiciones_graficas}","")
        cursor.execute(SQL_GRAFICAS)
        rows = cursor.fetchone()[0]
    except Exception as e:
        print(e)
        rows = []
    finally:
        cursor.close()
    return rows


def get_grafica_compuesta_query_sql(sql_graficas, condiciones_graficas):
    SQL_GRAFICAS = sql_graficas
    cursor = connection.cursor()
    try:
        if condiciones_graficas:
            SQL_GRAFICAS = SQL_GRAFICAS.format(condiciones_graficas = " AND " + condiciones_graficas)
        else:
            SQL_GRAFICAS = SQL_GRAFICAS.replace("{condiciones_graficas}","")
        cursor.execute(SQL_GRAFICAS)
        resultado = {
            "label":[],
            "values":[],
            "porcentaje":[],
        }
        rows = cursor.fetchall()
        for row in rows:
            resultado["label"].append(row[0])
            resultado["values"].append(row[1])
            try:
                resultado["porcentaje"].append(row[2])
            except Exception as e:
                pass
    except Exception as e:
        resultado = {
            "label":[],
            "values":[],
        }
    finally:
        cursor.close()
    return resultado


def get_grafica_para_tabla_query_sql(sql_graficas, condiciones_graficas):
    SQL_GRAFICAS = sql_graficas
    cursor = connection.cursor()
    try:
        if condiciones_graficas:
            SQL_GRAFICAS = SQL_GRAFICAS.format(condiciones_graficas = " AND " + condiciones_graficas)
        else:
            SQL_GRAFICAS = SQL_GRAFICAS.replace("{condiciones_graficas}","")
        cursor.execute(SQL_GRAFICAS)
        
        resultado = []
        rows = cursor.fetchall()
        titulos = [column[0] for column in cursor.description]
        for row in rows:
            registro = {}
            for aux in range(0,len(row)):
                registro[titulos[aux]] = row[aux]
            resultado.append(registro)

    except Exception as e:
        resultado = [
        ]
    finally:
        cursor.close()
    return resultado


def generador_excel(consulta, condiciones_graficas, excel_file_path='resultado_query.xlsx'):
    try:
        SQL_GRAFICAS = consulta
        if condiciones_graficas:
            SQL_GRAFICAS = SQL_GRAFICAS.format(condiciones_graficas = " AND " + condiciones_graficas)
        else:
            SQL_GRAFICAS = SQL_GRAFICAS.replace("{condiciones_graficas}","")
        df = pd.read_sql_query(SQL_GRAFICAS, connection)
        df.to_excel(excel_file_path, index=False)
        return excel_file_path
    except Exception as e:
        print(f"Error: {e}")
        return None