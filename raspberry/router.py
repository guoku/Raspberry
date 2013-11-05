class AuthRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'auth'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'auth'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'auth' or obj2._meta.app_label == 'auth':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'auth':
            return model._meta.app_label == 'auth'
        elif model._meta.app_label == 'auth':
            return False
        return None
