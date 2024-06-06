from flask_login import current_user

class CheckRole:
    def __init__(self,record=None):
        self.record = record
        
    def create(self):
        return current_user.is_admin()
    
    def show(self):
        return True
    
    def edit(self):
        if current_user.id == self.record.id:
            return True
        return current_user.is_admin()
    
    def delete(self):
        return current_user.is_admin()

    def view_index(self):
        return True

    def view_by_routes(self):
        return current_user.is_admin()

    def view_by_users(self):
        return current_user.is_admin()
