import aiohttp
from bs4 import BeautifulSoup
from telethon import TelegramClient,events
from specs import id,hash,admins
import random


#build the class
class client(TelegramClient) :
    def __init__(self, name, api_id, api_hash):
        super().__init__(name, api_id, api_hash)
        
        #اضافه كردن هندلري كه با اومدن ايونت جديد،تابع اصلي رو صدا ميزنه         
        self.add_event_handler(self.main, events.NewMessage)
        
    
    async def main(self,event) :
        
        #وارد شدن به يو آر ال يكي از غزل هاي حافظ در سايت گنجور بطور رندوم  
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session :
            ghazal_num = random.randint(0, 496) 
            url = f'https://ganjoor.net/hafez/ghazal/sh{ghazal_num}'
            
            #get response from the url
            async with session.get(url) as response:
                data = await response.text()
                
                #تميز كاري ريسپانس و جدا كردنه شعر از توش
                bs = BeautifulSoup(data , 'html.parser')
                
                mesra1_list = bs.find_all('div' , class_= 'b')
                poem = ''
                counter = 1
                
                for beit in mesra1_list :
                    new_beit = ''.join(f'{beit.text}')
                    poem += f'{counter}_\n{new_beit}\n{24*"-"}\n'
                    counter += 1  
                    
                #send the poem     
                await event.reply(poem)  
                raise events.StopPropagation      
                     
bot = client('user', id, hash)
bot.start('...')
bot.run_until_disconnected()                


