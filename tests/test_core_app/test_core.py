"""Test for the home view"""
import pytest
from unittest.mock import patch
from src.apps.core.tasks import automatic_reminder


def test_home_rendered(client) -> None:
    """Test the home route"""

    response = client.get('')
    assert response.status_code == 200


@patch('src.apps.core.tasks.send')
@pytest.mark.django_db
def test_automatic_scheduler_task_succeeds(send_email, add_due_reservations):
    automatic_reminder()
    assert send_email.called
    assert len(send_email.call_args_list) == 2


@patch('src.apps.core.tasks.send')
@pytest.mark.django_db
def test_automatic_scheduler_task_with_ticket_succeeds(send_email,
                                                       add_due_tickets):
    automatic_reminder()
    assert send_email.called
