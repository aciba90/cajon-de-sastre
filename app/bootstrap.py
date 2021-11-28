import inspect
from typing import Callable
# from app.adapters import redis_eventpublisher
from app.service import handlers, messagebus, unit_of_work


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)


def bootstrap(
    uow: unit_of_work.UnitOfWork = unit_of_work.MongoUnitOfWork(),
    publish: Callable = None  # redis_eventpublisher.publish,
) -> messagebus.MessageBus:

    dependencies = {"uow": uow, "publish": publish}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

