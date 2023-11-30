# NAME - имя владельца-узла, которому принадлежит запись о ресурсе
# TYPE - код типа RR
# CLASS - код класса RR
# TTL - временной интервал, в течение которого запись может кэшироваться
# прежде, чем снова возникнет необходимость обращения к источнику данных
# RDLENGTH - размер поля RDATA
# RDATA - строка переменного размера, описывающая ресурс

class ResourceRecord:
    def __init__(self, name, type, _class, ttl, rdlength, rdata):
        self.NAME = name
        self.TYPE = type
        self.CLASS = _class
        self.TTL = ttl
        self.RDLENGTH = rdlength
        self.RDATA = rdata
