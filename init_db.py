from sqlalchemy import create_engine
from model.models import Base

# Example for SQLite
engine = create_engine('sqlite:///112_calls.db')

# Or for PostgreSQL:
# engine = create_engine("postgresql://user:password@localhost:5432/112calls")

Base.metadata.create_all(engine)
print("✅ Database initialized.")