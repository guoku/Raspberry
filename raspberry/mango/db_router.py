class MangoRouter(object):
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mango':
            return 'mango'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mango':
            return 'mango'
        return None

    def allow_syncdb(self, db, model):
        if db == 'mango':
            return model._meta.app_label == 'mango'
        elif model._meta.app_label == 'mango':
            return False
        return None
