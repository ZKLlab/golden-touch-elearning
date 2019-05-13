点石成金网络教学平台（开发中）

[![Build Status](https://www.travis-ci.org/ZKLlab/golden-touch-elearning.svg?branch=dev)](https://www.travis-ci.org/ZKLlab/golden-touch-elearning)

## 环境要求

Python 3.7

## 开发环境配置

### 后端

#### 快速开始

1. 安装MySQL，创建数据库；
2. 进入项目文件夹，启动测试服务器：

```shell
$ pip3 install --upgrade pipenv
$ pipenv install
$ pipenv shell
(golden-touch-elearning) $ export SECRET_KEY=your_secret_key
(golden-touch-elearning) $ export MYSQL_DB=elearning_dev
(golden-touch-elearning) $ export MYSQL_USER=elearning_dev
(golden-touch-elearning) $ export MYSQL_PASS=your_mysql_password
(golden-touch-elearning) $ export MYSQL_HOST=localhost
(golden-touch-elearning) $ export MYSQL_PORT=3306
(golden-touch-elearning) $ python manage.py makemigrations
(golden-touch-elearning) $ python manage.py migrate
(golden-touch-elearning) $ python manage.py runserver 5000
```

#### 配置持久化保留

```shell
(golden-touch-elearning) $ cp testserver.py mytestserver.py
```

修改`mytestserver.py`文件中的配置，之后就可以用`mytestserver.py`代替`manage.py`而不用每次export环境变量，如：

```shell
(golden-touch-elearning) $ python mytestserver.py makemigrations
(golden-touch-elearning) $ python mytestserver.py migrate
(golden-touch-elearning) $ python mytestserver.py runserver 5000
```

### 前端

#### 快速开始

1. 安装[Vue CLI](https://cli.vuejs.org/zh/guide/installation.html)：

```shell
(golden-touch-elearning) $ npm install -g @vue/cli
# OR
(golden-touch-elearning) $ yarn global add @vue/cli
```

2. 配置环境

```shell
(golden-touch-elearning) $ cd frontend
(golden-touch-elearning) $ npm install
```

3. 启动服务

```shell
(golden-touch-elearning) $ npm run serve
# OR
(golden-touch-elearning) $ vue ui
```