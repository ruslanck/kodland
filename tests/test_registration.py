import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_new_user_with_not_new_name(setup_database, connection):
    add_user("kokp", "koko@gmail.com", "koko")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='koko';")
    user = cursor.fetchone()
    assert user, "пользователь уже зарегистрирован в базе(с данным логином)"

def test_authenticate_user(username, password):
    add_user("koko", "koko@g.c","koko")
    assert authenticate_user("koko", "koko") == True, "пользователь аунтефицирован"

def test_not_authenticate_user(username, password):
    assert authenticate_user("koko", "koko") == False, "пользователь не аунтефицирован"

def test_not_true_password_authenticate_user(username, password):
    add_user("koko", "koko@g.c","koko")
    assert authenticate_user("koko", "kok") == False, "неправильный пароль"

def test_display_users():
    add_user("koko", "koko@g.c","koko")
    assert display_users() == "Логин: koko, Электронная почта: koko@g.c", "список пользователей"

# Возможные варианты тестов:
"""
# Тест добавления пользователя с существующим логином.
# Тест успешной аутентификации пользователя.
# Тест аутентификации несуществующего пользователя.
# Тест аутентификации пользователя с неправильным паролем.
# Тест отображения списка пользователей.
"""