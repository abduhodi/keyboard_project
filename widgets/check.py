import re
class Check:
    def is_valid_email(self):
        if re.match(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", self):
            return True
        else:
            return False


    def is_valid_name(self):
        if len(self) < 2 or (not self.isalpha()):
            return False
        else:
            return True


    def is_valid_passwd(self):
        if len(self) < 8:
            return False
        if not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}", self):
            return False
        else:
            return True


    def is_valid_id(self):
        if not (7 < len(self) < 12 and self.isdigit()):
            return  False
        else:
            return True
