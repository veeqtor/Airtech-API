"""Module to test the check db command"""

from subprocess import PIPE, Popen


class TestCheckDB:
    """
    Class representing the test for the check db command.
    """

    def test_check_db_success(self) -> None:
        """
        Test the check db command.
        """
        p = Popen(['python', 'manage.py', 'checkDB'],
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode

        assert output.decode('utf-8') == \
            'Waiting for database...\nDatabase available!\n'
        assert rc == 0
