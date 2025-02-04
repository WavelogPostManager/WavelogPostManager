import unittest
from unittest.mock import patch
from wavelogpostmanager.server.server_runner import ServerRunner


class TestServerRunner(unittest.TestCase):
    @patch("wavelogpostmanager.server.server_runner.SignoffProcessor.create_new_queue_mysql")
    def test_queue_request_NoQueuedQSL_ReturnsQueueNoList(self, mock_create_new_queue_mysql):
        mock_create_new_queue_mysql.return_value = (-5, [], [])
        result = ServerRunner.queue_request({})
        self.assertEqual(result, {"return_code": 200, "action": "queue_no_list"})

if __name__ == "__main__":
    unittest.main()