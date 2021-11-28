from app.service.unit_of_work import MongoUnitOfWork
from app.domain.models import Word


# TODO make a proper test

with MongoUnitOfWork() as uow:
    word = Word("asdfa", 0, 123)
    uow.words.add(word)
    uow.commit()
    # uow.rollback()
    words = uow.words.list()
    print(list(words))
