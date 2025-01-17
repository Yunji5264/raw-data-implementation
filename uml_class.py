import json

class DS_Spatial_Granularity:
    def __init__(self, spatialGranularity):
        self.spatialGranularity = spatialGranularity

    def to_dict(self):
        return {"spatialGranularity": self.spatialGranularity}

    @classmethod
    def from_dict(cls, data):
        return cls(data["spatialGranularity"])


class DS_Temporal_Granularity:
    def __init__(self, temporalGranularity):
        self.temporalGranularity = temporalGranularity

    def to_dict(self):
        return {"temporalGranularity": self.temporalGranularity}

    @classmethod
    def from_dict(cls, data):
        return cls(data["temporalGranularity"])


class DS_Spatial_Scope:
    def __init__(self, spatialScopeLevel, spatialScope):
        self.spatialScopeLevel = spatialScopeLevel
        self.spatialScope = spatialScope

    def to_dict(self):
        return {
            "spatialScopeLevel": self.spatialScopeLevel,
            "spatialScope": self.spatialScope
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["spatialScopeLevel"], data["spatialScope"])


class DS_Temporal_Scope:
    def __init__(self, temporalScopeLevel, temporalScopeStart, temporalScopeEnd):
        self.temporalScopeLevel = temporalScopeLevel
        self.temporalScopeStart = temporalScopeStart
        self.temporalScopeEnd = temporalScopeEnd

    def to_dict(self):
        return {
            "temporalScopeLevel": self.temporalScopeLevel,
            "temporalScopeStart": self.temporalScopeStart,
            "temporalScopeEnd": self.temporalScopeEnd
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["temporalScopeLevel"],
            data["temporalScopeStart"],
            data["temporalScopeEnd"]
        )


class DS_Space:
    def __init__(self, spatialGranularity, spatialScope):
        self.spatialGranularity = spatialGranularity
        self.spatialScope = spatialScope

    def to_dict(self):
        return {
            "spatialGranularity": self.spatialGranularity.to_dict(),
            "spatialScope": self.spatialScope.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        spatial_granularity = DS_Spatial_Granularity.from_dict(data["spatialGranularity"])
        spatial_scope = DS_Spatial_Scope.from_dict(data["spatialScope"])
        return cls(spatial_granularity, spatial_scope)


class DS_Time:
    def __init__(self, temporalGranularity, temporalScope):
        self.temporalGranularity = temporalGranularity
        self.temporalScope = temporalScope

    def to_dict(self):
        return {
            "temporalGranularity": self.temporalGranularity.to_dict(),
            "temporalScope": self.temporalScope.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        temporal_granularity = DS_Temporal_Granularity.from_dict(data["temporalGranularity"])
        temporal_scope = DS_Temporal_Scope.from_dict(data["temporalScope"])
        return cls(temporal_granularity, temporal_scope)


class DS_Space_Time:
    def __init__(self, space, time):
        self.space = space
        self.time = time

    def to_dict(self):
        return {
            "space": self.space.to_dict(),
            "time": self.time.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        space = DS_Space.from_dict(data["space"])
        time = DS_Time.from_dict(data["time"])
        return cls(space, time)


class DS_Theme:
    def __init__(self, themeCode, themeDescription):
        self.themeCode = themeCode
        self.themeDescription = themeDescription

    def to_dict(self):
        return {
            "themeCode": self.themeCode,
            "themeDescription": self.themeDescription
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["themeCode"], data["themeDescription"])


class DS_Identification:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def to_dict(self):
        return {"title": self.title, "description": self.description}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["description"])


class DS_Ingestion:
    def __init__(self, dataFormat, fileType, updateFrequency, sourceName, sourceType, sourceAddress):
        self.dataFormat = dataFormat
        self.fileType = fileType
        self.updateFrequency = updateFrequency
        self.sourceName = sourceName
        self.sourceType = sourceType
        self.sourceAddress = sourceAddress

    def to_dict(self):
        return {
            "dataFormat": self.dataFormat,
            "fileType": self.fileType,
            "updateFrequency": self.updateFrequency,
            "sourceName": self.sourceName,
            "sourceType": self.sourceType,
            "sourceAddress": self.sourceAddress
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["dataFormat"],
            data["fileType"],
            data["updateFrequency"],
            data["sourceName"],
            data["sourceType"],
            data["sourceAddress"]
        )

# Data_Content
class Data_Content:
    def __init__(self, dataName, dataDescription, dataType):
        self.dataName = dataName
        self.dataDescription = dataDescription
        self.dataType = dataType

    def to_dict(self):
        return {
            "dataName": self.dataName,
            "dataDescription": self.dataDescription,
            "dataType": self.dataType
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["dataName"], data["dataDescription"], data["dataType"])


# subclass：Parameter
class Parameter(Data_Content):
    def __init__(self, dataName, dataDescription, dataType, parameterCode):
        super().__init__(dataName, dataDescription, dataType)
        self.parameterCode = parameterCode

    def to_dict(self):
        data = super().to_dict()
        data["parameterCode"] = self.parameterCode
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["dataName"],
            data["dataDescription"],
            data["dataType"],
            data["parameterCode"]
        )


# subclass：Spatial_Parameter
class Spatial_Parameter(Parameter):
    def __init__(self, dataName, dataDescription, dataType, parameterCode, spatialLevel):
        super().__init__(dataName, dataDescription, dataType, parameterCode)
        self.spatialLevel = spatialLevel

    def to_dict(self):
        data = super().to_dict()
        data["spatialLevel"] = self.spatialLevel
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["dataName"],
            data["dataDescription"],
            data["dataType"],
            data["parameterCode"],
            data["spatialLevel"]
        )


# subclass：Temporal_Parameter
class Temporal_Parameter(Parameter):
    def __init__(self, dataName, dataDescription, dataType, parameterCode, temporalLevel):
        super().__init__(dataName, dataDescription, dataType, parameterCode)
        self.temporalLevel = temporalLevel

    def to_dict(self):
        data = super().to_dict()
        data["temporalLevel"] = self.temporalLevel
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["dataName"],
            data["dataDescription"],
            data["dataType"],
            data["parameterCode"],
            data["temporalLevel"]
        )


# subclass：Complementary_Information
class Complementary_Information(Data_Content):
    def __init__(self, dataName, dataDescription, dataType, ciCode, related_parameter):
        super().__init__(dataName, dataDescription, dataType)
        self.ciCode = ciCode
        self.related_parameter = related_parameter

    def to_dict(self):
        data = super().to_dict()
        data["ciCode"] = self.ciCode
        if isinstance(self.related_parameter, (Spatial_Parameter, Temporal_Parameter)):
            data["related_parameter"] = self.related_parameter.to_dict()
        else:
            data["related_parameter"] = None  # Safely handle None or unrecognized types
        return data

    @classmethod
    def from_dict(cls, data):
        related_parameter_data = data.get('related_parameter')
        related_parameter = None
        if related_parameter_data:
            if 'spatialLevel' in related_parameter_data:
                related_parameter = Spatial_Parameter.from_dict(related_parameter_data)
            elif 'temporalLevel' in related_parameter_data:
                related_parameter = Temporal_Parameter.from_dict(related_parameter_data)

        return cls(
            data["dataName"],
            data["dataDescription"],
            data["dataType"],
            data["ciCode"],
            related_parameter
        )

# subclass：Existing_Indicator
class Existing_Indicator(Data_Content):
    def __init__(self, dataName, dataDescription, dataType, indicatorCode):
        super().__init__(dataName, dataDescription, dataType)
        self.indicatorCode = indicatorCode

    def to_dict(self):
        data = super().to_dict()
        data["indicatorCode"] = self.indicatorCode
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["dataName"],
            data["dataDescription"],
            data["dataType"],
            data["indicatorCode"]
        )


class Dataset:
    def __init__(self, identification, ingestion, space_time, theme, data_content):
        """
        Represents a Dataset with identification, ingestion, space-time, themes, and data content.

        :param identification: DS_Identification object
        :param ingestion: DS_Ingestion object
        :param space_time: DS_Space_Time object
        :param theme: DS_Theme object
        :param data_content: List of Data_Content or its subclasses
        """
        self.identification = identification  # DS_Identification object
        self.ingestion = ingestion  # DS_Ingestion object
        self.space_time = space_time  # DS_Space_Time object
        self.theme = theme  # DS_Theme object
        self.data_content = data_content  # List[Data_Content] objects (or its subclasses)

    def to_dict(self):
        """
        Serialize the Dataset object into a dictionary format.
        """
        return {
            "identification": self.identification.to_dict(),
            "ingestion": self.ingestion.to_dict(),
            "space_time": self.space_time.to_dict(),
            "theme": self.theme.to_dict(),
            "data_content": [content.to_dict() for content in self.data_content]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserialize a dictionary into a Dataset object.

        :param data: Dictionary containing the dataset structure.
        """
        identification = DS_Identification.from_dict(data["identification"])
        ingestion = DS_Ingestion.from_dict(data["ingestion"])
        space_time = DS_Space_Time.from_dict(data["space_time"])
        theme = DS_Theme.from_dict(data["theme"])
        # Dynamically map `data_content` to their respective subclasses
        data_content = [
            cls._map_to_subclass(content)
            for content in data["data_content"]
        ]
        return cls(identification, ingestion, space_time, theme, data_content)

    @staticmethod
    def _map_to_subclass(data):
        """
        Map dictionary data to the appropriate subclass of Data_Content based on keys.
        """
        if "parameterCode" in data and "spatialLevel" in data:
            return Spatial_Parameter.from_dict(data)
        elif "parameterCode" in data and "temporalLevel" in data:
            return Temporal_Parameter.from_dict(data)
        elif "ciCode" in data:
            return Complementary_Information.from_dict(data)
        elif "indicatorCode" in data:
            return Existing_Indicator.from_dict(data)
        elif "parameterCode" in data:
            return Parameter.from_dict(data)
        else:
            return Data_Content.from_dict(data)

    def save_to_json(self, file_path):
        """
        Save the Dataset object to a JSON file.

        :param file_path: Path where the JSON file will be saved.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    @classmethod
    def load_from_json(cls, file_path):
        """
        Load a Dataset object from a JSON file.

        :param file_path: Path to the JSON file.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

