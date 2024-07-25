In the Ports and Adapters (Hexagonal) architecture, also known as Clean Architecture, a background job service like Celery would typically be considered a **secondary adapter**.

### Explanation

#### Primary Adapters
Primary adapters (or driving adapters) are the ones that initiate interactions with the application. They represent the entry points into the system. Examples include:

- HTTP controllers (e.g., FastAPI endpoints)
- CLI commands
- Scheduled jobs

#### Secondary Adapters
Secondary adapters (or driven adapters) are the ones that the application interacts with to fulfill its operations. They represent the external systems and services that the application depends on. Examples include:

- Databases
- Message brokers (e.g., Redis)
- External APIs
- Background job processors (e.g., Celery)

### Background Job Service as a Secondary Adapter

A background job service like Celery:

1. **Provides Services to the Core:** The core application (domain and application logic) uses Celery to offload tasks that need to be executed asynchronously or outside the main request-response cycle.
2. **Is Invoked by the Core:** The application initiates background tasks by sending jobs to Celery, but Celery itself does not drive the application's core logic.
3. **Depends on External Infrastructure:** Celery relies on a message broker like Redis or RabbitMQ to queue and manage tasks, making it an external dependency.

### Integration in Ports and Adapters Architecture

In a typical ports and adapters setup, you might have:

- **Ports:** Interfaces defined in the core application for sending background jobs.
- **Adapters:** Implementation of these interfaces using Celery.

#### Example

1. **Port Definition (Interface):**

```python
# ports.py
from abc import ABC, abstractmethod

class BackgroundJobPort(ABC):
    @abstractmethod
    def send_task(self, task_name: str, *args, **kwargs):
        pass
```

2. **Adapter Implementation (Celery Adapter):**

```python
# adapters.py
from celery import Celery
from ports import BackgroundJobPort

celery_app = Celery(
    'worker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

class CeleryAdapter(BackgroundJobPort):
    def send_task(self, task_name: str, *args, **kwargs):
        celery_app.send_task(task_name, args=args, kwargs=kwargs)
```

3. **Application Use:**

```python
# application.py
from ports import BackgroundJobPort

class TaskService:
    def __init__(self, job_port: BackgroundJobPort):
        self.job_port = job_port

    def perform_task(self, data):
        # Perform some synchronous logic
        # ...

        # Send a background task
        self.job_port.send_task('my_background_task', data)
```

By setting it up this way, you keep the core application logic decoupled from the specifics of Celery, making it easier to replace Celery with another background job processor in the future if needed.