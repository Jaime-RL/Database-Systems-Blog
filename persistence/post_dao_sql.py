import psycopg2
from psycopg2.extras import DictCursor

from business.entities.post import Post

from persistence import connection_manager
from persistence.post_dao import PostDao


class PostDaoSql(PostDao):

    def find_by_id(self, post_id):
        post = None

        try:
            conn = connection_manager.get_connection()
            cursor = conn.cursor(cursor_factory=DictCursor)

            query = """ select post_id, subject, body from post where post_id = %s """
            cursor.execute(query, [post_id])

            result = cursor.fetchone()
            if result is not None:
                post = self.map_post(result)

            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print("ERROR:\n{0}".format(e))

        return post

    def find_posts(self):
        return self.__find_many(""" select post_id, subject, body from post order by post_id """)

    def find_posts_by_blog(self, blog_id):
        """Devuelve los posts de un blog concreto (usado al cargar un blog completo)."""
        return self.__find_many(
            """ select post_id, subject, body from post where blog_id = %s order by post_id """,
            [blog_id],
        )

    def insert_post(self, post):
        return self.__execute_single_row(
            """ insert into post(post_id, subject, body) values (%s, %s, %s) """,
            (post.get_id(), post.get_subject(), post.get_body()),
        )

    def update_post(self, p):
        return self.__execute_single_row(
            """ update post set subject = %s, body = %s where post_id = %s """,
            (p.get_subject(), p.get_body(), p.get_id()),
        )

    def delete_post(self, p):
        return self.__execute_single_row(
            """ delete from post where post_id = %s """,
            [p.get_id()],
        )

    def map_post(self, result):
        """
        Devuelve un objeto post con los datos del resultado de la consulta
        """
        return Post(id=result["post_id"], subject=result["subject"], body=result["body"])

    # ------------------------------------------------------------------
    # Métodos auxiliares: evitan repetir el mismo patrón conexión/cursor
    # ------------------------------------------------------------------

    def __find_many(self, query, parameters=None):
        posts = []

        try:
            conn = connection_manager.get_connection()
            cursor = conn.cursor(cursor_factory=DictCursor)
            cursor.execute(query, parameters or [])

            for result in cursor.fetchall():
                posts.append(self.map_post(result))

            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print("ERROR:\n{0}".format(e))

        return posts

    def __execute_single_row(self, query, parameters):
        """Ejecuta un insert/update/delete y devuelve True si afectó exactamente a una fila."""
        result = False

        try:
            conn = connection_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            result = cursor.rowcount == 1

            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print("ERROR:\n{0}".format(e))

        return result
