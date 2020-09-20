import redis


class RedisSingleton:
    __instance = None

    def __init__(self):
        raise Exception("This class is a Singleton! Please use get_instance method.")

    @staticmethod
    def get_instance():
        if not RedisSingleton.__instance:
            RedisSingleton.__instance = redis.Redis('localhost')
        return RedisSingleton.__instance
