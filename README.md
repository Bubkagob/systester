### Список модулей

SYSTESTER пакет содержит в себе модули:

* [Volcano] - Обёртка для управлением процессом Corex
* [client61850] - Клиент МЭК 61850 (автотесты), основанный на Libiec61850
* [restapi] - клиент для взаимодействия с libweb компонентом Volcano (основанн на requests модуле)


### Установка

При исполнении установочного скрипта, будет произведена проверка на зависимости и/или их установка

```sh
$ python setup.py install
```


### Зависимости

Требуемые библиотеки:

* [libiec61850] - при cmake-генерации использовать ключ -DBUILD_PYTHON_BINDINGS=ON
* [lxml] - xml парсер
* [requests] - Http для людей
* [pymodbus] - Протокол Modbus
### Todos

 - добавить документацию на модули
 - добавить примеры


   [libiec61850]: <https://github.com/mz-automation/libiec61850>
   [lxml]: <https://github.com/lxml/lxml>
   [requests]: <https://github.com/requests/requests>
   [pymodbus]: <https://github.com/riptideio/pymodbus>