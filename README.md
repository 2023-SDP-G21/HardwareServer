
# Hardware Server
### Setup Guide
1. Clone the repository to your local machine
2. Run `poetry install` in the root to install packages

### Information
A socket is created which runs two separate threads - one for receiving data, and another for sending data. The data to be sent is collected and processed from the sensors as well as warnings. For more information on this data please refer to the API Documentation.