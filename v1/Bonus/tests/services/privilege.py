import asyncio

import pytest

from app.services.exceptions import UserNotFoundError, UsernameAlreadyExistError
from app.presentation.api.schemas import PrivilegeResponse


class TestPrivilegeService:
    def test_create_new_user_success(self, privilege_service, mock_privilege_repository):
        username = "newuser"
        mock_privilege_repository.get_user.return_value = None
        mock_privilege_repository.create_new_user.return_value = 1

        asyncio.run(privilege_service.create_new_user(username))

        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.create_new_user.assert_awaited_once_with(username)

    def test_create_new_user_already_exists(self, privilege_service, mock_privilege_repository, sample_user):
        username = "testuser"
        mock_privilege_repository.get_user.return_value = sample_user

        with pytest.raises(UsernameAlreadyExistError) as exc_info:
            asyncio.run(privilege_service.create_new_user(username))

        assert exc_info.value.username == username
        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.create_new_user.assert_not_awaited()

    def test_delete_user_success(self, privilege_service, mock_privilege_repository, sample_user):
        username = "testuser"
        mock_privilege_repository.get_user.return_value = sample_user

        asyncio.run(privilege_service.delete_user(username))

        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.delete_user.assert_awaited_once_with(username)

    def test_delete_user_not_found(self, privilege_service, mock_privilege_repository):
        username = "nonexistent"
        mock_privilege_repository.get_user.return_value = None

        with pytest.raises(UserNotFoundError) as exc_info:
            asyncio.run(privilege_service.delete_user(username))

        assert exc_info.value.username == username
        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.delete_user.assert_not_awaited()

    def test_get_user_success(self, privilege_service, mock_privilege_repository, sample_user):
        username = "testuser"
        mock_privilege_repository.get_user.return_value = sample_user

        result = asyncio.run(privilege_service.get_user(username))

        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        assert isinstance(result, PrivilegeResponse)
        assert result.id == sample_user.id
        assert result.username == sample_user.username
        assert result.status == sample_user.status
        assert result.balance == sample_user.balance

    def test_get_user_not_found(self, privilege_service, mock_privilege_repository):
        username = "nonexistent"
        mock_privilege_repository.get_user.return_value = None

        with pytest.raises(UserNotFoundError) as exc_info:
            asyncio.run(privilege_service.get_user(username))

        assert exc_info.value.username == username
        mock_privilege_repository.get_user.assert_awaited_once_with(username)

    def test_set_user_balance_success(self, privilege_service, mock_privilege_repository, sample_user):
        username = "testuser"
        new_balance = 500
        mock_privilege_repository.get_user.return_value = sample_user

        asyncio.run(privilege_service.set_user_balance(username, new_balance))

        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.set_balance.assert_awaited_once_with(username, new_balance)

    def test_set_user_balance_user_not_found(self, privilege_service, mock_privilege_repository):
        username = "nonexistent"
        new_balance = 500
        mock_privilege_repository.get_user.return_value = None

        with pytest.raises(UserNotFoundError) as exc_info:
            asyncio.run(privilege_service.set_user_balance(username, new_balance))

        assert exc_info.value.username == username
        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.set_balance.assert_not_awaited()

    def test_change_user_balance_success(self, privilege_service, mock_privilege_repository, sample_user):
        username = "testuser"
        balance_diff = 50
        initial_balance = sample_user.balance
        expected_balance = initial_balance + balance_diff
        mock_privilege_repository.get_user.return_value = sample_user

        asyncio.run(privilege_service.change_user_balance(username, balance_diff))

        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.set_balance.assert_awaited_once_with(username, expected_balance)

    def test_change_user_balance_negative(self, privilege_service, mock_privilege_repository, sample_user):
        username = "testuser"
        balance_diff = -30
        initial_balance = sample_user.balance
        expected_balance = initial_balance + balance_diff
        mock_privilege_repository.get_user.return_value = sample_user

        asyncio.run(privilege_service.change_user_balance(username, balance_diff))

        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.set_balance.assert_awaited_once_with(username, expected_balance)

    def test_change_user_balance_user_not_found(self, privilege_service, mock_privilege_repository):
        username = "nonexistent"
        balance_diff = 50
        mock_privilege_repository.get_user.return_value = None

        with pytest.raises(UserNotFoundError) as exc_info:
            asyncio.run(privilege_service.change_user_balance(username, balance_diff))

        assert exc_info.value.username == username
        mock_privilege_repository.get_user.assert_awaited_once_with(username)
        mock_privilege_repository.set_balance.assert_not_awaited()
