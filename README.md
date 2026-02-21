# 📚 FastAPI + SQLite – Learning Exercise Project

This README is AI generated (because of course it is).

## 🔥⚠️ IMPORTANT – THIS IS A LEARNING/REFRESHING PROJECT ⚠️🔥

This repository exists **purely for educational purposes**.

I am actively learning/refreshing:

* FastAPI
* REST API design
* Dependency injection
* SQLite integration
* CRUD operations
* HTTP methods (GET, POST, PUT, PATCH, DELETE)

There are **known issues**, **intentional shortcuts**, and **non-production patterns** in this code.

That is expected.

This is a sandbox to understand:

* how FastAPI works internally
* how request/response flow behaves
* how to structure endpoints
* how database connections work with dependencies
* what NOT to do in production

---

## 🚨 What This Project Is NOT

This is **NOT**:

* production-ready
* secure
* optimized
* following best practices fully
* protected against SQL injection
* using ORM
* using Pydantic models properly
* architecturally clean

This is a controlled environment for experimentation.

---

## 🧠 What I Am Practicing Here

* Creating versioned endpoints (`/api/v1/...`)
* Using dependency injection (`Depends`)
* Basic SQLite connection handling
* Manual SQL queries
* Random record selection
* Partial updates (`PATCH`)
* REST semantics

---

## 🔥 Yes, I Know There Are Problems

Examples of intentional simplifications:

* Raw f-string SQL queries (unsafe)
* No validation layer
* No error handling for missing records
* No response models
* No async
* No ORM
* No repository layer
* No separation of concerns

That’s the point.

I want to understand the fundamentals before abstracting them away.

---

## 🎯 Goal of This Repository

To deeply understand:

* What happens before introducing SQLAlchemy
* What happens before introducing Pydantic schemas
* What happens before introducing authentication
* What happens before introducing proper architecture

First principles > abstraction.

---

## 🚀 How to Run

```bash
uvicorn main:app --reload
```

Then open:

```
http://127.0.0.1:8000/docs
```

---

## 🛠 Tech Stack

* Python
* FastAPI
* SQLite
* Uvicorn

---

## 📈 Future Improvements (When I’m Ready)

* Replace raw SQL with parameterized queries
* Add Pydantic models
* Add proper error handling
* Add async DB access
* Introduce SQLAlchemy
* Add tests
* Improve architecture

---

## Final Note

This repo documents the learning process — not the final level.

If you’re reviewing this code:

Yes, I see the problems.
Yes, they are intentional.
Yes, I am improving step by step.

---

