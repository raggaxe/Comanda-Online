import re

def mask_email(email):
    email_split = re.search(r'(.+)@(.+)\.(.+)', email)
    if email_split:
        username, domain_front, *domain_back_list = list(email_split.groups())
        username_masked = username[0] + 'x' * (len(username) - 1)
        domain_front_masked = domain_front[0]+ 'x' * (len(domain_front)-1)
        domain_back = '.'.join(domain_back_list)
        return '{}@{}.{}'.format(username_masked, domain_front_masked, domain_back)

def maskEmail(email):
    lo = email.find('@')
    if lo > 0 :
        return email[0]+'#####'+email[lo-1:]
    else:
        return 'email inválido'
