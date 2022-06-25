from db_helpers import run_query
class Crud:

    def get_user_by_token(self, token: str):
        query = f"SELECT * FROM client_session WHERE token = '{token}'"
        client_id = run_query(query)
        return client_id


    def get_restaurant_by_token(self, token: str):
        query = f"SELECT * FROM restaurant_session WHERE token = '{token}'"
        client_id = run_query(query)
        return client_id
