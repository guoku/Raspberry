class AuthRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.app_label == 'mobile' or model._meta.app_label == 'base':
            return 'auth'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.app_label == 'mobile' or model._meta.app_label == 'base':
            return 'auth'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return None
