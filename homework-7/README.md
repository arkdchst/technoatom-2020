Тестируемое приложение - `google_app/`, его описание [здесь](https://github.com/arkdchst/2020-2-Atom-QA-Python-A-Chistyj/blob/111e7ddf5f0e57b1f89c86dae4aa810d08c1ce0c/homework-6/README.md)

Для того, чтоб собрать ДЗ, необходимо:

1. запустить скрипт `./build.sh`, который соберёт Docker-образ приложения с запущенным `SSH` для мониторинга
2. запустить приложение `./start_google_app.sh`
3. запустить тесты
	* Яндекс.Танк - `./start_yandex_tank.sh`
	* locust - `./start_locust.py`

*Все имена вымышленные, любые совпадения случайны*