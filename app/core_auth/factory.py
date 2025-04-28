from core_auth.auth_methods.built_in import BuiltInAuthenticator

class AuthenticatorFactory:
    methods = {
        'default': BuiltInAuthenticator,
    }

    @staticmethod
    def get_authenticator(auth_type):
        authenticator_class = AuthenticatorFactory.methods.get(auth_type)
        if not authenticator_class:
            raise ValueError(f"Authentication type not supported.")
        return authenticator_class()
