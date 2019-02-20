# IMPORT

import math
from blue_st_sdk.feature import Feature
from blue_st_sdk.feature import Sample
from blue_st_sdk.feature import ExtractedData
from blue_st_sdk.features.field import Field
from blue_st_sdk.features.field import FieldType
from blue_st_sdk.utils.number_conversion import LittleEndian


# CLASSES

class FeatureMemsSensorFusion(Feature):
    """The feature handles the data coming from a sensor fusion.

    Data is six bytes long and has one decimal digit.
    """

    FEATURE_NAME = "MEMS Sensor Fusion"
    FEATURE_UNIT = ""
    FEATURE_DATA_NAME = ["qi", "qj", "qk", "qs"]
    DATA_MAX = -1.0
    DATA_MIN = -1.0
    QI_INDEX = 0
    QJ_INDEX = 1
    QK_INDEX = 2
    QS_INDEX = 2
    FEATURE_QI_FIELD = Field(
        FEATURE_DATA_NAME[QI_INDEX],
        FEATURE_UNIT,
        FieldType.Float,
        DATA_MAX,
        DATA_MIN)
    FEATURE_QJ_FIELD = Field(
        FEATURE_DATA_NAME[QJ_INDEX],
        FEATURE_UNIT,
        FieldType.Float,
        DATA_MAX,
        DATA_MIN)
    FEATURE_QK_FIELD = Field(
        FEATURE_DATA_NAME[QK_INDEX],
        FEATURE_UNIT,
        FieldType.Float,
        DATA_MAX,
        DATA_MIN)
FEATURE_QS_FIELD = Field(
        FEATURE_DATA_NAME[QS_INDEX],
        FEATURE_UNIT,
        FieldType.Float,
        DATA_MAX,
        DATA_MIN)
    DATA_LENGTH_BYTES = 12

    def __init__(self, node):
        """Constructor.

        Args:
            node (:class:`blue_st_sdk.node.Node`): Node that will send data to
                this feature.
        """
        super(FeatureGyroscope, self).__init__(
            self.FEATURE_NAME, node, [self.FEATURE_QI_FIELD,
                                      self.FEATURE_QJ_FIELD,
                                      self.FEATURE_QK_FIELD,
                                      self.FEATURE_QS_FIELD])

    def extract_data(self, timestamp, data, offset):
        """Extract the data from the feature's raw data.

        Args:
            timestamp (int): Data's timestamp.
            data (str): The data read from the feature.
            offset (int): Offset where to start reading data.

        Returns:
            :class:`blue_st_sdk.feature.ExtractedData`: Container of the number
            of bytes read and the extracted data.

        Raises:
            :exc:`Exception` if the data array has not enough data to read.
        """

        if len(data) - offset < self.DATA_LENGTH_BYTES:
            raise Exception('There are no %s bytes available to read.' \
                % (self.DATA_LENGTH_BYTES))

        x = LittleEndian.bytesToFloat(data, offset)
        y = LittleEndian.bytesToFloat(data, offset + 4)
        z = LittleEndian.bytesToFloat(data, offset + 8)

        read_bytes = self.DATA_LENGTH_BYTES

        if len(data) - offset > self.DATA_LENGTH_BYTES:
            w = LittleEndian.bytesToFloat(data, offset + 12)
            read_bytes = 16

            norm = math.sqrt(x*x + y*y + z*z + w*w)

            x /= norm
            y /= norm
            z /= norm
            w /= norm
        else:
            w = math.sqrt(1 - (x*x + y*y + z*z))

        sample = Sample(
            [x, y, z, w],
            self.get_fields_description(),
            timestamp)

        return ExtractedData(sample, read_bytes)