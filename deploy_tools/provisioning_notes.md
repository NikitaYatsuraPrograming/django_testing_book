## Необходимые пакеты:

* Nginx
* Python
* virtualenv + pip
* Git

## Конфигурация виртуального узла Nginx 

* см. nginx.template.conf
* создать переменную окружения $SERVER_NAME
* изменить в nginx.conf user(на того у кого есть право просматривать папку sites)

## Структура папок
/root
|____sites
     |____SERVER_NAME
	  |----db
	  |----source
	  |----static
	  |----virtualenv
