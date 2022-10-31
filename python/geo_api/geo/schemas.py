import datetime
from pydantic import BaseModel
import dataclasses


@dataclasses.dataclass
class GeoInfo(BaseModel):
    geonameid: int
    name: str
    asciiname: str
    alternatenames: str
    latitude: float
    longitude: float
    feature_class: str
    feature_code: str
    country_code: str
    cc2: str
    admin1_code: str
    admin2_code: str
    admin3_code: str
    admin4_code: str
    population: int
    elevation: str
    dem: str
    timezone: str
    modification_date: datetime.date


# @dataclasses.dataclass
class GeoInfoCompare(BaseModel):
        north: str
        is_same_time: bool
        timezone_diff: str
        name_1: GeoInfo
        name_2: GeoInfo
