import os
import manage

if __name__ == '__main__':
    os.environ.setdefault('SECRET_KEY', 'your_secret_key')
    os.environ.setdefault('MYSQL_DB', 'elearning_dev')
    os.environ.setdefault('MYSQL_USER', 'elearning_dev')
    os.environ.setdefault('MYSQL_PASS', 'your_mysql_password')
    os.environ.setdefault('MYSQL_HOST', 'localhost')
    os.environ.setdefault('MYSQL_PORT', '3306')
    os.environ.setdefault('ALIYUN_ACCESS_KEY_ID', '')
    os.environ.setdefault('ALIYUN_ACCESS_KEY_SECRET', '')
    os.environ.setdefault('ALIYUN_VOD_CATE_ID', '')

    manage.main()
