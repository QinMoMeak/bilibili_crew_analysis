import csv
import json
import urllib.request
import requests
import re
import os
import time
 
class marine:
 
    total= 0         #大航海总数
    lv6Count = 0
    lv5Count = 0
    lv4Count = 0
    lv3Count = 0
    lv2Count = 0
    lv1Count = 0
    lv0Count = 0
    ship1Count = 0   #总督
    ship2Count = 0   #提督
    ship3Count = 0   #舰长
    uid = ''
    ruid = ''
    user_space = ''
    all_page=0       #舰长列表页数
    crew_list='./crew_list/'#存放舰长列表的文件夹名称
    header = {
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
 
    def __init__(self,uid):
        self.uid = uid
        self.space = 'https://api.bilibili.com/x/space/acc/info?mid='+uid+'&jsonp=jsonp'#用户信息
        
    def ruid(self):#根据uid获取直播间号
        # space_request = urllib.request.Request(self.space,headers=self.header)
        # space_html = urllib.request.urlopen(space_request).read().decode('utf-8')
        # self.ruid = re.findall(r'live.bilibili.com/(.*?)"',space_html)[0]
        self.ruid='25512501'
        print("直播间号：",self.ruid)

        self.caplist = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid='+self.ruid+'&page=1&ruid='+self.uid+'&page_size=29'#直播间信息
        
    def Snapshot(self):#下载舰长列表
        
        if not os.path.exists(self.crew_list):
            os.makedirs(self.crew_list)
 
        request = urllib.request.Request(self.caplist,headers=self.header)
        reponse = urllib.request.urlopen(request).read()
 
        path=self.crew_list+'page1.html'
        fh = open(path,"wb")    
        fh.write(reponse)
        fh.close()
        
        reponse=reponse.decode('utf-8')
        all_page = re.findall(r'"page":(.*?),',reponse)[0]    
        self.all_page=int(all_page)
        
        total = re.findall(r'"num":(.*?),',reponse)[0]
        self.total=int(total)
        
        print("舰长总数：",self.total)
 
        for i in range(2,self.all_page+1):
            time.sleep(0.5)
            caplist = 'https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid='+self.ruid+'&page='+str(i)+'&ruid='+self.uid+'&page_size=29'#舰长列表网址
            request = urllib.request.Request(caplist,headers=self.header)
            reponse = urllib.request.urlopen(request).read()
 
            path = self.crew_list+'page'+str(i)+'.html'
            fh = open(path,"wb")    
            fh.write(reponse)
            fh.close()
            
    def count(self):#开始统计
        
        dirs = os.listdir(self.crew_list)
        crew_list=[]
        flag=[]
        
        for i in range(0,self.total+1):
            flag.append(0)
        
        for file in dirs:#将船员uid、舰队等级、舰队排序存放于三元组列表
            path = self.crew_list + file
            fd = open(path,encoding='utf-8')
            content=fd.read()
            crew_list.extend(re.findall(r'"uid":(.*?),"ruid":.*?"rank":(.*?),"username":".*?","face":".*?","is_alive":.*?,"guard_level":(.*?),',content))
            fd.close()
            # print(crew_list)
            list(set(crew_list))
 
        for each in crew_list:#统计舰长、提督、总督数量
            
            if int(each[2])==3 and flag[int(each[1])]==0:
                self.ship3Count+=1
                flag[int(each[1])]=1
                
            elif int(each[2])==2 and flag[int(each[1])]==0:
                self.ship2Count+=1
                flag[int(each[1])]=1
                
            elif int(each[2])==1 and flag[int(each[1])]==0:
                self.ship1Count+=1
                flag[int(each[1])]=1
 
        for i in range(0,self.total+1):
            flag[i]=0
        counter=0
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),end='')
        print("开始统计船员等级")
        index_crew = len(crew_list) - 1
        # for each in crew_list:#统计船员等级
        while index_crew >=0:
            each = crew_list[index_crew]
            # if flag[int(each[1])]==0:
            time.sleep(1)
            # flag[int(each[1])]=1
            counter+=1
            if counter%30==0:
                print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),end='')
                print("\033[30m完成度：%5d/%5d\033[0m"%(counter,self.total))

            uid = str(each[0])
            url = 'https://api.bilibili.com/x/space/wbi/acc/info?mid='+uid
            request = requests.get(url=url,headers=self.header)
            reponse = str(request.text)
            # reponse = reponse.encode("utf-8")
            print("index_crew:"+str(index_crew))

            print("uid:"+uid+"level:",end='')
            json_data= json.loads(reponse)

            if json_data['code']!=0:
                index_crew += 1
                # print("@@@@@@@index_crew:"+str(index_crew))

            else:
                lv = json_data['data']['level']
                print(lv)
                filename = "data.csv"  # Specify the CSV file name
                name = json_data['data']['name']
                mid = json_data['data']['mid']
                level = json_data['data']['level']
                with open(filename, "a", encoding="utf-8", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([name, mid, level])
                    
                # print(counter)
                # lv = data['level']
                # # print(reponse)
                # lv=re.findall(r'"level":(.*?),"jointime"',reponse)[0]
                if int(lv)==6:
                    self.lv6Count+=1
                elif int(lv)==5:
                    self.lv5Count+=1
                elif int(lv)==4:
                    self.lv4Count+=1
                elif int(lv)==3:
                    self.lv3Count+=1
                elif int(lv)==2:
                    self.lv2Count+=1
                elif int(lv)==1:
                    self.lv1Count+=1
                elif int(lv)==0:
                    self.lv0Count+=1
            index_crew -= 1
        # print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),end='')
        print("船员等级统计完成")
        
    def display(self):#展示统计结果
 
        print("--------------------------------")
        
        print("6级号：%5d/%d，占比：% 2.3f%%"%(self.lv6Count,self.total,self.lv6Count*1.0/self.total*100))
        print("5级号：%5d/%d，占比：% 2.3f%%"%(self.lv5Count,self.total,self.lv5Count*1.0/self.total*100))
        print("4级号：%5d/%d，占比：% 2.3f%%"%(self.lv4Count,self.total,self.lv4Count*1.0/self.total*100))
        print("3级号：%5d/%d，占比：% 2.3f%%"%(self.lv3Count,self.total,self.lv3Count*1.0/self.total*100))
        print("2级号：%5d/%d，占比：% 2.3f%%"%(self.lv2Count,self.total,self.lv2Count*1.0/self.total*100))
        print("1级号：%5d/%d，占比：% 2.3f%%"%(self.lv1Count,self.total,self.lv1Count*1.0/self.total*100))
        print("0级号：%5d/%d，占比：% 2.3f%%"%(self.lv0Count,self.total,self.lv0Count*1.0/self.total*100))
        
        print("总督： %5d/%d，占比：% 2.3f%%"%(self.ship1Count,self.total,self.ship1Count*1.0/self.total*100))
        print("提督： %5d/%d，占比：% 2.3f%%"%(self.ship2Count,self.total,self.ship2Count*1.0/self.total*100))
        print("舰长： %5d/%d，占比：% 2.3f%%"%(self.ship3Count,self.total,self.ship3Count*1.0/self.total*100))
        
        print("--------------------------------")
        
 
 
uid='1795147802'
jiaran=marine(uid)
jiaran.ruid()
jiaran.Snapshot()
jiaran.count()
jiaran.display()
 