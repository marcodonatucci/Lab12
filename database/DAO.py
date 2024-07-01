from database.DB_connect import DBConnect
from model.retailer import Retailer
from model.edges import edges


class DAO:
    @staticmethod
    def getCountry():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gr.Country 
FROM go_retailers gr
ORDER BY gr.Country"""
            cursor.execute(query)
            for row in cursor:
                result.append(row['Country'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getRetailers(country):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT gr.*
FROM go_retailers gr
WHERE gr.Country = %s"""
            cursor.execute(query, (str(country),))
            for row in cursor:
                result.append(Retailer(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(year, country, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT gr.Retailer_name as id1, gr2.Retailer_name  as id2, COUNT(DISTINCT gds2.Product_number) as weight
FROM go_retailers gr, go_retailers gr2, go_daily_sales gds, go_daily_sales gds2 
WHERE gr2.Retailer_code < gr.Retailer_code and gr2.Retailer_code = gds2.Retailer_code and gr.Retailer_code = gds.Retailer_code and gds2.Product_number = gds.Product_number and YEAR(gds2.`Date`) = YEAR(gds.`Date`) and YEAR(gds2.`Date`) = %s and gr.Country = gr2.Country and gr2.Country = %s
GROUP BY id1, id2
"""
            cursor.execute(query, (year, country))
            for row in cursor:
                result.append(edges(idMap[row['id1']], idMap[row['id2']], row['weight']))
            cursor.close()
            cnx.close()
        return result
