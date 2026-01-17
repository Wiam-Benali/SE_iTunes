from database.DB_connect import DBConnect
from model.album import Album
from model.collegamenti import Collegamenti


class DAO:
    @staticmethod
    def leggi_album(d):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  distinct a.id, a.title, sum(milliseconds)/60000 as durata
                    FROM album a, track t
                    WHERE a.id = t.album_id
                    GROUP BY a.id, a.title
                    HAVING sum(milliseconds)/60000 > %s"""

        cursor.execute(query, (d,))

        for row in cursor:
            result[row['id']] = (Album(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def leggi_collegamenti(album,d):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query =     """ WITH valid_albums AS (SELECT distinct a.id
                                                FROM album a, track t
                                                WHERE a.id = t.album_id
                                                GROUP BY a.id
                                                HAVING sum(milliseconds)/60000 > %s)
                                                
                        SELECT t1.album_id as album1_id, t2.album_id as album2_id
                        FROM playlist_track p1, track t1, playlist_track p2, track t2
                        WHERE p1.track_id = t1.id and  p2.track_id = t2.id  and p2.playlist_id = p1.playlist_id and t1.album_id > t2.album_id
                             and t1.album_id IN (SELECT id FROM valid_albums) and  t2.album_id IN (SELECT id FROM valid_albums)
                        GROUP by t1.album_id, t2.album_id """

        cursor.execute(query,(d,))
        for row in cursor:
            a1 = album[row['album1_id']]
            a2 = album[row['album2_id']]
            result.append(Collegamenti(a1,a2))
        cursor.close()
        conn.close()
        return result

