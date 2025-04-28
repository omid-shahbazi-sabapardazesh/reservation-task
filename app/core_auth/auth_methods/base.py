from abc import ABC, abstractmethod

class BaseAuthenticator(ABC):
    @abstractmethod
    def authenticate(self, request):
        pass
