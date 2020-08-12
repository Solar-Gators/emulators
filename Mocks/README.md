# Mocks
This module contains definitions for hardware within the car. These modules inhearit from the Message ABC
## Structuring a mock
Mocks are free to be constructed however you want so long as they create messages in the same way the recieving system expects them. Most mocks have their items structured in a way that the class can self iterate and get the items in the required order. Mocks should represent the hardware they emulate.