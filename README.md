
# Hardware Server
### Setup Guide
1. Clone the repository to your local machine
2. Run `bluetooth.py` to connect to startup the bluetooth connection

### Information
A socket is created which runs two separate threads - one for receiving data, and another for sending data. 
The data to be sent is collected and processed from the sensors as well as warnings. For more information on this data 
please refer to the API Documentation. 

The connection is established using the `socket` python library over a bluetooth connection. 

### Running the Test Suite
Ensure that you have `pytest` installed. If not, run `pip install pytest` in your terminal.

To run all the tests in the test suite simply run `pytest tests/` in the root directory of the project. This recursively
runs all the unit tests and integration tests in the `tests` directory.