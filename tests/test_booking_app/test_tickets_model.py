"""Test module for the ticket model"""

import pytest

from tests.fixtures.ticket import NEW_TICKET

pytestmark = pytest.mark.django_db


class TestTicketModel:
    """Test ticket model"""

    def test_the_model_string_succeeds(self, add_tickets):
        """Test that ticket model string rep is correct."""

        ticket = add_tickets[0]
        assert ticket.__str__(
        ) == f'{ticket.ticket_ref} - {ticket.seat_number}'

    def test_ticket_creation_succeeds(self, add_tickets):
        """
        Test that a ticket model can be successfully created.
        """
        ticket = add_tickets[0]

        assert ticket.flight is not None
        assert ticket.seat_number is not None
        assert ticket.made_by is not None
        assert ticket.date_made is not None
        assert ticket.ticket_ref == NEW_TICKET[0]['ticket_ref']

    def test_ticket_deletion_succeeds(self, add_tickets):
        """
        Test ticket deletion
        """

        ticket = add_tickets[0]
        ticket.delete()

        assert ticket.deleted

    def test_ticket_hard_deletion_succeeds(self, add_tickets):
        """
        Test ticket hard deletion
        """

        ticket = add_tickets[0]
        ticket.hard_delete()

        assert ticket.id is None
