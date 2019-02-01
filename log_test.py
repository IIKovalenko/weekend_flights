import logging

# Существует пять уровней логирования (в порядке возрастания): DEBUG, INFO, WARNING, ERROR и CRITICAL

# прочесть: http://python-lab.blogspot.com/2013/03/blog-post.html

logging.basicConfig(filename="sample.log", level=logging.INFO) # для вывода логов в файл
# logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)3d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO) # для вывода логов в консоль

logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")


print('hello')
