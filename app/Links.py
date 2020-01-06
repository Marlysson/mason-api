"""Links Model."""

from config.database import Model

class Links(Model):
    
    __hidden__ = ['id', 'updated_at', 'alias']

    def get_date_format(self):
        return "01.06.2020"