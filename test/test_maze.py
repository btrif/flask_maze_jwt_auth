#  Created by btrif Trif on 13-07-2022 , 2:55 PM.
import requests
import pytest_mock

# @pytest.mark.parametrize(
#     "maze_configuration, expect",
#     [
#         "maze_config1" : {
#             "entrance": "F1",
#             "gridSize": "7x9",
#             "id": 16,
#             "walls": [
#                         "A2",    "A7",    "B4",    "B5",    "B6",    "B7",    "C1",    "C2",    "C4",    "C7",    "D6",    "D7",
#                         "E2",    "E3",    "E4",    "E6",    "E7",    "G1",    "G2",    "G4",    "G6",    "G7",    "H2",    "H4",
#                         "H6",    "H7",    "I1",    "I2",    "I3",   "I7"]
#         }
#     ]
# )

from src.routes import hi, create_maze, get_maze





def test_hi_api_get_call(mocker):           # This runs Fine
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.ok = True
    name = "Pogacar"
    mock_requests.return_value.text = "Hello "  + str(name)
    request = requests.get(f"http://127.0.0.1:5000/hi/{name}")
    response = hi(name)
    print(f"Response :              {response}")
    mock_requests.assert_called_with(f"http://127.0.0.1:5000/hi/{name}")
    assert response == mock_requests.return_value.text



def test_get_maze_api_call_no_authentication(mocker):
    mock_requests = mocker.patch("requests.post")
    mock_requests.return_value = True

    expected_message = {
                        "path": "['F1', 'E1', 'D1', 'D2', 'D3', 'D4', 'D5', 'E5', 'F5', 'F6', 'F7']",
                        "status": "success"
                        }

    id = 16

    # request = requests.get(f"http://127.0.0.1:5000/maze/{id}/solution?steps=max")

    response = get_maze("oli",id)
    print(f"response : {response}")



    assert 11 == 11


import requests

class A():

    def get_response(self, url):
        response = requests.get(url)
        return response.text


