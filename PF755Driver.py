from pycomm3 import CIPDriver, Services, ClassCode, BOOL, BYTE, STRING, REAL, ResponseError, DataType
from typing import Union, Optional, Tuple, List, Sequence, Type, Any, Dict


class PF755Driver(object):

    ip_address = ""
    connection = None

    def __init__(self, ip_address: str):
        """
        :return:
        """
        self.ip_address = ip_address
        self.connection = CIPDriver(self.ip_address)

    def open(self):
        """

        :return:
        """
        self.connection.open()

    def close(self):
        self.connection.close()

    def write_parameter(self, port: int, parameter: int, value: Any, data_type: Optional[Union[Type[DataType], DataType]] = None):

        instance = parameter + 0 if port <= 0 else 1024 * port + 17408
        self.connection.generic_message(
            service=Services.set_attribute_single,
            class_code=b"\x9F",  # 0x9F = DPI Parameter
            attribute=b"\x0A",  # parameter value attribute
            request_data=data_type.encode(value),
            instance=instance,
            data_type=data_type
        )

    def read_parameter(self, port: int, parameter: int, data_type: Optional[Union[Type[DataType], DataType]] = None):
        """
        :param port:
        :param parameter:
        :return:

        See https://literature.rockwellautomation.com/idc/groups/literature/documents/um/750com-um001_-en-p.pdf

        Page 117
        The instance is the parameter number in the drive (Port 0). For example, to write to Parameter 4 of a
        peripheral in Port 5 of a PowerFlex 755 drive, the instance would be 21504 + 4 = 21508.
        See DPI Parameter Object on page 169 (Class code 0x93) or Host DPI Parameter Object on page 184
        (Class code 0x9F) to determine the instance
        number.

        Page 169
        Instances Device Example Description
        (Hex.) (Dec.)
        0x0000…0x3FFF 0…16383 Host Drive 0 Class Attributes (Drive) (difference of 0x3FFF or 30 bits)
        0x4000…0x43FF 16384…17407 Adapter 1 Drive Parameter 1 Attributes (difference of 1023)
        0x4400…0x47FF 17408…18431 Port 1 2 Drive Parameter 2 Attributes (difference of 1023)
        0x4800…0x4BFF 18432…19455 Port 2 …
        0x4C00…0x4FFF 19456…20479 Port 3 16384 Class Attributes (Adapter)
        0x5000…0x53FF 20480…21503 Port 4 16385 Adapter Parameter 1 Attributes
        0x5400…0x57FF 21504…22527 Port 5 …
        0x5800…0x5BFF 22528…23551 Port 6
        0x5C00…0x5FFF 23552…24575 Port 7
        0x6000…0x63FF 24576…25599 Port 8
        0x6400…0x67FF 25600…26623 Port 9
        0x6800…0x6BFF 26624…27647 Port 10
        0x6C00…0x6FFF 27648…28671 Port 11
        0x7000…0x73FF 28672…29695 Port 12
        0x7400…0x77FF 29696…30719 Port 13
        0x7800…0x7BFF 30720…31743 Port 14
        """

        instance = parameter + 0 if port <= 0 else 1024 * port + 17408



        response = self.connection.generic_message(
            service=Services.get_attribute_single,
            class_code=b"\x9F",  # 0x9F = DPI Parameter
            attribute=b"\x0A",  # parameter value attribute
            instance=instance,
            data_type=data_type if data_type is not None else REAL
        )

        if not response:
            raise (ResponseError(f"Response did not return valid data - {response.error}"))

        print(f"{port}\t{parameter}\t{response.value}")

        return response
