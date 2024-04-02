def test_get_user_by_id(manager_service, created_user):
    user = manager_service.get_user_by_id(user_id=created_user.id)

    assert user.id == created_user.id


def test_update_user_verified_status(manager_service, created_user):
    manager_service.update_user_verified_status(
        user_id=created_user.id, status=True
    )

    assert (
        manager_service.get_user_by_id(user_id=created_user.id).verified
        is True
    )
