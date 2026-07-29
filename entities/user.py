from api.api_manager import ApiManager


class User:
    """Модель пользователя, хранит креды, роли и свой Apimanager,
    через который пользователь выполняет запросы под своей ролью"""


    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api  # экземпляр ApiManager для запросов от имени этого юзера

    @property
    def creds(self):
        """Возвращает кортеж (email, passwod)"""
        return self.email, self.password