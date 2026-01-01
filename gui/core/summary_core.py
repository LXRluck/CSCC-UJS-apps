import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from PySide6.QtCore import QObject, Signal

class Summary(QObject):
    progress = Signal(str, int)
    finished = Signal(bool, str)
    summary_result = Signal(list)

    def __init__(self, srt_path, txt_path, topK):
        """初始化"""
        super().__init__()
        self.srt_path = srt_path
        self.isrunning = True
        self.topK = topK
        self.txt_path = txt_path

        # 存储提取的摘要语句
        self.sentences = []

    def swap(self):
        """文本类型转换"""
        sub = load(self.srt_path)  
        convert(sub, self.txt_path)

    def abstract_sum(self):
        try:
            self.progress.emit("正在生成摘要...", 30)
            text = codecs.open(self.txt_path, 'r', 'utf-8').read()
            tr4w = TextRank4Keyword()
        
            self.progress.emit("正在生成摘要...", 50)
            tr4w.analyze(text=text, lower=True, window=2)

            self.progress.emit("正在生成摘要...", 70)
            tr4s = TextRank4Sentence()
            tr4s.analyze(text=text, lower=True, source='all_filters')

            self.progress.emit("正在生成摘要...", 90)
            # 获取关键句，返回的是包含 sentence 等字段的字典列表
            self.sentences = tr4s.get_key_sentences(num=self.topK)
            # 发送摘要内容信号
            self.summary_result.emit(self.sentences)
            # 发送完成信号，提示成功
            self.finished.emit(True, "摘要生成成功！")
        except Exception as e:
            self.finished.emit(False, f"生成摘要失败: {str(e)}")
            raise

    def run(self):
        self.swap()

        self.abstract_sum()

    def stop(self):
        self.isrunning = False

def load(path):
    if path.split(".")[len(path.split("."))-1]=="lrc":
        hh_list = []
        mm_list = []
        ss_list = []
        mms_list = []
        content_list = []
        file = open(path,"r",encoding="utf-8")
        sub = file.readlines()
        sub[0]=sub[0][1:len(sub[0])+1]
        file.close()
        for n in sub:
            n = n.strip(" ")
            n = n.strip("[")
            content = n.split("]")[1]
            time = n.split("]")[0]
            hh_list.append(str(int(time.split(':')[0])//60).rjust(2,'0'))
            mm_list.append(str(int(time.split(':')[0])%60).rjust(2,'0'))
            ss_list.append(str(time.split(':')[1].split('.')[0]).rjust(2,'0'))
            mms_list.append(str(time.split(':')[1].split('.')[1]).ljust(3,'0'))
            content_list.append(content)
        finallist = [hh_list,mm_list,ss_list,mms_list,content_list]
        return(finallist)
    
    if path.split(".")[len(path.split("."))-1]=="srt":
        hh_list = []
        mm_list = []
        ss_list = []
        mms_list = []
        content_list = []
        file = open(path,"r",encoding="utf-8")
        sub = file.readlines()
        sub[0]=str(0)
        file.close()
        a= 0
        for n in sub:
            n=n.strip('\n')
            if n.isdecimal() :
                time = sub[int(a)+1].split(' --> ')[0]
                hh = str((time.split(':')[0]))
                mm = str((time.split(':')[1]))
                ss = str(time.split(',')[0].split(':')[2])
                mms =  str(time.split(',')[1])
                content = sub[a+2]
                hh_list.append(hh)
                mm_list.append(mm)
                ss_list.append(ss)
                mms_list.append(mms)
                content_list.append(content)
            a = a+1
    finallist = [hh_list,mm_list,ss_list,mms_list,content_list]
    return(finallist)


def convert(data,path):
    if path.split(".")[len(path.split("."))-1]=="txt":
        content_list = data[4]
        file = open(path,"w",encoding="utf-8")
        for a in content_list:
            file.write(a)
        file.close()
     
    if path.split(".")[len(path.split("."))-1]=="lrc":
        hh_list = data[0]
        mm_list = data[1]
        ss_list = data[2]
        mms_list = data[3]
        content_list = data[4]
        file = open(path,"w",encoding="utf-8")
        for a in range(len(mm_list)):
            file.write('['+mm_list[a]+':'+ss_list[a]+'.'+mms_list[a]+']'+content_list[a])
        file.close()
            
    if path.split(".")[len(path.split("."))-1]=="srt":
        hh_list = data[0]
        mm_list = data[1]
        ss_list = data[2]
        mms_list = data[3]
        content_list = data[4]
        file = open(path,"w",encoding="utf-8")
        hh_list.append(hh_list[len(hh_list)-1])
        mm_list.append(mm_list[len(mm_list)-1])
        ss_list.append(int(ss_list[len(ss_list)-1])+5)
        mms_list.append(mms_list[len(mms_list)-1])
        for a in range(len(hh_list)-1):
            file.write(str(a)+'\n')
            file.write(str(hh_list[a])+':'+str(mm_list[a])+':'+str(ss_list[a])+','
                       +str(mms_list[a])+" --> "+str(hh_list[a+1])+':'+str(mm_list[a+1])
                       +':'+str(ss_list[a+1])+','+str(mms_list[a+1])+'\n')
            file.write(content_list[a]+'\n')
        file.close()