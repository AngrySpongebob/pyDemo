import threading
import queue
import time



api_url = "http://www.baidu.com?page="


def main(url_queue):
	while True:
		try:
			url = url_queue.get_nowait()
			# a = url_queue.qsize()
			time.sleep(.5)
		except Exception as e:
			print("退出")
			break
		else:
			pass
		finally:
			pass
		pass
		print(f'当前的URL是：{url}')

if __name__ == '__main__':

	start_time_p = time.time()  # 程序运行开始时间
	url_queue = queue.Queue()  # 创建空队列
	for i in range(10):
		url = api_url + str(i+1)
		url_queue.put(url)  # 将所有的url放入队列中

	threads = []
	thread_num = 2
	for _ in range(thread_num):
		t = threading.Thread(target=main, args=(url_queue, ))
		threads.append(t)

	for t in threads:
		t.start()

	for t in threads:
		# 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
		t.join()
	end_time_p = time.time()  # 程序结束时间
	print(f'Done, Time cost: {end_time_p - start_time_p}')

