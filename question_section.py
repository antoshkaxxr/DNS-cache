# Вопросительный раздел передаёт "вопрос" в большинстве запросов (т.е.
# параметры, определяющие что нужно узнать). Он включает в себя
# QDCOUNT элементов:
# QNAME - доменное имя
# QTYPE - тип запроса
# QCLASS - класс запроса

class QuestionSection:
    def __init__(self, qname, qtype, qclass):
        self.QNAME = qname
        self.QTYPE = qtype
        self.QCLASS = qclass
