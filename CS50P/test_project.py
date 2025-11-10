from project import create_master_password, validate_master_password, select_mode, store_password, view_password
import pytest
import os
import bcrypt
  

def test_create_master_password(monkeypatch):
    """ Mock input function """
    def mock_input(prompt):
        return "1111"
    
    """ Temporarily replace the input function with the mock function """
    monkeypatch.setattr('builtins.input', mock_input)

    create_master_password()

    """ Checking if the master password file is created """
    assert os.path.exists('master_password.txt')

    """ Checking if the master password file contains the hashed password """
    with open('master_password.txt', 'r') as file:
        hashed_password = file.read()
    assert bcrypt.checkpw('1111'.encode(), hashed_password.encode())
    

def test_validate_master_password(monkeypatch):
    """ Validating the correct master password """
    monkeypatch.setattr('builtins.input', lambda _: '1111')
    validate_master_password()

    """ Validating the incorrect master password """
    monkeypatch.setattr('builtins.input', lambda _: '1234')
    with pytest.raises(SystemExit):
        validate_master_password()


def test_select_mode(monkeypatch):
    """ Mock user input for selecting mode 1 """
    monkeypatch.setattr('builtins.input', lambda _: '1')
    assert select_mode() is store_password

    """ Mock user input for selecting mode 2 """
    monkeypatch.setattr('builtins.input', lambda _: '2')
    assert select_mode() is view_password

    """ Mock user input for selecting mode 3 """
    monkeypatch.setattr('builtins.input', lambda _: '3')
    with pytest.raises(SystemExit):
        select_mode()


def test_store_password(monkeypatch, tmpdir):
    """ Setting up a mock master password """
    monkeypatch.setattr('builtins.input', lambda _: '1111')

    """ Setting up a password file """
    tmp_password_file = str(tmpdir.join('password.txt'))

    """ Change the current directory to working directory """
    tmpdir.chdir()

    """ Checking if the password file is created """
    assert not os.path.exists(tmp_password_file)
    store_password()
    assert os.path.exists(tmp_password_file)


def test_view_password(monkeypatch, capfd):
    """ Mock input function """
    def mock_input(prompt):
        return "testuser"
    
    """ Temporarily replace the input function with the mock function """
    monkeypatch.setattr('builtins.input', mock_input)

    """ Calling view_password function to caputre it's output """
    store_password()
    view_password()
    
    """ Checking and capturing if the output is produced """
    out, err = capfd.readouterr()
    assert 'testuser' in out    