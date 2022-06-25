from faker import Faker
from dateutil.relativedelta import relativedelta
from random import randint,choice
import string


alphabet_string = string.ascii_lowercase
alphabet_list = list(alphabet_string)


""" Create N users directly to company """ 
# for alhpabet in alphabet_list:
#     lahir = fake.date_of_birth()
#     join = lahir + relativedelta(years = randint(10,20), month= randint(1,12), days=randint(1,30))
#     refferal = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(8))
#     gender = 'Laki' if randint(0,1) else 'Perempuan'
#     query = "("+ alhpabet +":USER{nama: '" + fake.name() + "',lahir:date('"+ str(lahir) +"'),gender:'" + gender + "',refferal:'" + refferal + "'})-[:CHILD_OF{join:date('"+ str(join) +"')}]->(com),(com)-[:LEADERS_OF{join:date('"+ str(join) +"')}]->("+ alhpabet +"),\n"

#     with open('query.txt','a') as f:
#         f.write(query)

def create_random_user(prefix='',prev=''):
    fake = Faker()
    lahir = fake.date_of_birth()
    join = lahir + relativedelta(years = randint(10,20), month= randint(1,12), days=randint(1,30))
    refferal = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(8))
    gender = 'Laki' if randint(0,1) else 'Perempuan'
    return "("+ prefix + alhpabet +":USER{nama: '" + fake.name() + "',lahir:date('"+ str(lahir) +"'),gender:'" + gender + "',refferal:'" + refferal + "'})-[:CHILD_OF{join:date('"+ str(join) +"')}]->("+ alhpabet +"),("+ alhpabet +")-[:LEADERS_OF{join:date('"+ str(join) +"')}]->("+ i + alhpabet +"),\n"

""" Create N users relationship to a-z """ 
for i in ['a','b','c']:
    for alhpabet in alphabet_list:
        
        query = create_random_user(prefix=i)
        with open('query.txt','a') as f:
            f.write(query)

        if randint(0,4) == 0:
            x_prefix= i + 'x'
            query2 = create_random_user(prefix=x_prefix,prev=i)
            with open('query.txt','a') as f:
                f.write(query2)

            if randint(0,2) == 0:
                y_prefix= i + 'y'
                query3 = create_random_user(prefix=y_prefix,prev=x_prefix)
                with open('query.txt','a') as f:
                    f.write(query3)

                if randint(0,2) == 0:
                    z_prefix= i + 'z'
                    query4 = create_random_user(prefix=z_prefix,prev=y_prefix)
                    with open('query.txt','a') as f:
                        f.write(query4)

                    if randint(0,1) == 0:
                        w_prefix= i + 'w'
                        query5 = create_random_user(prefix=w_prefix,prev=z_prefix)
                        with open('query.txt','a') as f:
                            f.write(query5)

                        if randint(0,1) == 0:
                            s_prefix= i + 's'
                            query6 = create_random_user(prefix=s_prefix,prev=w_prefix)
                            with open('query.txt','a') as f:
                                f.write(query6)

                            if randint(0,1) == 0:
                                t_prefix= i + 't'
                                query7 = create_random_user(prefix=t_prefix,prev=s_prefix)
                                with open('query.txt','a') as f:
                                    f.write(query7)