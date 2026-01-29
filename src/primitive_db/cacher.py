def create_cacher():
    #кэшер
    cache = {}

    def cache_result(key, value_func):
        #возвращаем значение из кэша или вычисляем и сохраняем
        if key in cache:
            return cache[key]
        value = value_func()
        cache[key] = value
        return value

    return cache_result
