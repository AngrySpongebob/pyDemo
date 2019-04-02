from selenium import webdriver as wd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
import sys


# 进度条类
class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 50):
        self.count = count
        self.total = total
        self.width = width
    def move(self):
        self.count += 1
    def log(self, s=None):
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        progress = self.width * self.count / self.total
        sys.stdout.write("["+'#' * int(progress) + '_' * (self.width - int(progress)+"]"))
        sys.stdout.write('{2}:{0:3}/{1:3}: '.format(self.count, self.total, s) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print(path+'：创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+'：目录已存在')
        return False


# 获取每一页的小说列表，以及对应的链接
def pagelist(url, browser, wait):

	browser.get(url)
	main = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".main_con")))
	booknames = main.find_elements_by_class_name("bookname")
	bookname = []
	bookurl = []

	for j in booknames:
		
		atip = j.find_element_by_tag_name("a")
		bookname.append(atip.text)	
		bookurl.append(atip.get_attribute("href").replace("/book/","/showchapter/"))
			
	return (bookname,bookurl)


# 获取每本小说的章节		
def bookind(bookname, bookurl, browser, wait):
	
	browser.get(bookurl)
	chapterlisturl = []
	chapterlistname = []
	booklist = browser.find_elements_by_class_name("chapter-list")
	
	for boo in booklist:
		
		bookchapter = boo.find_elements_by_tag_name("li")  # 目录

		for m in bookchapter:

			chapterlistname.append(m.text)
			chapterlisturl.append(m.find_element_by_tag_name("a").get_attribute("href"))
		
	bar = ProgressBar(total = len(chapterlistname))  # 实例化进度条
	for i,j in zip(chapterlistname,chapterlisturl):
		try:
			browser.get(j)
			bookcount = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".content")))
			bookp = bookcount.find_elements_by_tag_name("p")
			bookdata = ""
			for n in bookp:
				bookdata = "    " + n.text + "\n" + bookdata
			
			with open("E:\\书\\{0}\\{1}.txt".format(bookname,i), "w+",encoding='utf8') as f:
				f.write(bookdata)

			bar.move()
			bar.log(bookname)
			time.sleep(0.5)
		except Exception as e:
			print(bookname+":"+i+"出现异常")
		else:
			pass
		finally:
			pass
		

def main(url):

  # 使用谷歌浏览器
	chrome_options = wd.ChromeOptions()
	chrome_options.add_argument('''Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36''')
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	prefs = {
		'profile.default_content_setting_values': {
			'images': 2
		}
	}
	chrome_options.add_experimental_option('prefs', prefs)
	browser = wd.Chrome('C:\\chromdriver\\chromedriver.exe',chrome_options=chrome_options)
	wait = WebDriverWait(browser, 3)
	sourcecode = browser.get(url)
	# 获取页数
	pagenumber =browser.find_element_by_class_name("pagenumber").get_attribute("count")
	
	for i in range(1,int(pagenumber)+1):
		booklists = "http://book.zongheng.com/store/c0/c0/b0/u0/p{}/v0/s1/t0/u0/i0/ALL.html".format(i)
		booknames,bookurls = pagelist(booklists, browser, wait)
		for j in booknames:

			mkpath="E:\\书\\{}\\".format(j)
			mkdir(mkpath)

		for bookname,bookurl in zip(booknames,bookurls):
			
			bookind(bookname, bookurl,browser, wait)
		

if __name__ == '__main__':
	url = "http://book.zongheng.com/store/c0/c0/b0/u0/p1/v0/s1/t0/u0/i0/ALL.html"
	main(url)
# print(maindata[0].text)
# data = ""
# try:
# 	# for i in main:
# 	# 	data += i.text

# 	with open("文档.txt", "w+") as f:
# 		f.write(main)
# except Exception as e:
# 	print(e)
# else:
# 	print("完成")
# finally:
# 	pass

