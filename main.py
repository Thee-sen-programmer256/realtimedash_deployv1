import faker
import logging, random, datetime
import pandas as pd,time,os

#create a faker object 
fake=faker.Faker()


#create qb transactions
def qb_transactions() -> dict:
    user=fake.simple_profile()
    return {
            'customer_id':f'000{str(random.randint(10000, 99999))}',
            'username': user['username'],
            'tran_id':f'S{str(random.randint(100,999))}',
            'tran_date':datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'operation':random.choice(['EFT','B2W','MOBI_EARLY_PAYMENT','BILK_B2W','W2B']),
            'status':random.choice(['Successfully-process','Transation-Failed']),
            'account_number': '0112226789087',
            'amount':round(random.uniform(1000,8000),2),
            'currency':random.choice(['UGX','USD']),
            'phone':fake.phone_number(),
            'branch':random.choice(['KYADONDO','NATETE','KIKUUBO','JINJA','SOROTI']),
            'region':random.choice(['NOTHERN','EASTERN','WESTERN','SOUTHERN']),
            'dest_bank':'DFCUBANK'
            }

if __name__=='__main__':
    id=0
    value_id=1
    while True:
        # to mysql
        transaction=pd.json_normalize(qb_transactions())
        tran_list=transaction.values[0]
        tran_list = [str(value) for value in tran_list]
        print(*tran_list)
        with open('{}/qb_live1.txt'.format(os.getcwd()),'a') as f:
            f.write(','.join(tran_list)+ '\n')
        id+=1
        value_id+=1
        #Truncate the file it 
        if value_id > 100:
            with open('{}/qb_live1.txt'.format(os.getcwd()), 'w') as f:
                f.truncate(0)
            value_id = 1 

        time.sleep(1)



    


