# oms运维管理系统 #

[![python3.x](https://img.shields.io/badge/python-3.X-blue.svg)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-1.11-blue.svg)](https://www.djangoproject.com/)
[![django-rest-framework](https://img.shields.io/badge/djangorestframework-3.6.3-blue.svg)](http://www.django-rest-framework.org/)
[![celery](https://img.shields.io/badge/celery-4.1.0-green.svg)](http://www.celeryproject.org/)
[![vue](https://img.shields.io/badge/vue-2.5.9-brightgreen.svg)](https://github.com/vuejs/vue)
[![element-ui](https://img.shields.io/badge/element--ui-2.0.7-brightgreen.svg)](https://github.com/ElemeFE/element)

注意：该项目是采用的前后端分离开发，是在python3.6下面开发的，因为是使用的django-rest-framework，理论也支持python2.7x；由于前端使用的是vuejs,所以不支持低版本ie游览器。

本项目集成工单系统、发布系统、dns和zabbix管理、saltstack管理。


[文档查看](https://itimor.github.io/django-oms/)

[线上demo](http://oms.itimor.cf/)  ### 地址已经失效

```
用户名：admin
密码: 有人喜欢删admin用户，具体长什么样子看文档吧
```

## 项目实践

### 1. 克隆项目
``` bash
git clone https://github.com/itimor/django-oms.git
```

### 2. 后端
```
# 安装python依赖
cd omsBackend
pip install -r requirements.txt

# 生成数据库文件
# 把每个模块 makemigrations
python manage.py makemigrations 模块名

#初始化数据库
python manage.py migrate

#创建admin用户
python manage.py createsuperuser 

#启动
python manage.py runserver 0.0.0.0:8000

```

### 3. 前端
```
# 安装依赖
npm install
#或者
npm install --registry=https://registry.npm.taobao.org

# 本地开发 开启服务
npm run dev

# 打包
npm run build
```

## 项目后续功能
- [ ] 周报系统
> 每周结束之前在oms系统上发布周报，方便领导统计、查看。

- [ ] 继续想新功能

> 本地查看文档

```
mkdocs serve --dev-addr=0.0.0.0:5000
mkdocs build
mkdocs gh-deploy
```
