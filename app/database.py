from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

"""
engine - двидок для подключения в БД. Хранит все настройки подключения и соединение с БД.
connect_args - настраивает однопотоковое соединение. Запрещает использовать это соединение в других потоках. 
SessionLocal - объект. Создает рабочую сессию с БД. С помощью нее делаются запросы в БД
sessionmaker - функция внутри библиотеки sqlalchemy, которая создает объект SessionLocal. 
 С помощью этой конструкции каждый запрос будет получать свое собственное соединение, окторое нужно будет выключать.
autocommit=False - сами решаем, когда коммитить нашу транзакцию. 
autoflush=False - сами хотим управлять тем, когда отправлять запрос в БД. Т.е. пишем конструкции/вызовы, 
но запрос будет проходить только тогда, когда мы укажем. Если autoflush=True, то эти действия происходят сразу.
bind=engine - подключили движок. 
"""

DATABASE_URL = "sqlite:///./finance.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
