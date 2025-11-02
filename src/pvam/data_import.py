# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 14:33:05 2025

@author: Annalise
"""

import geomag
import pandas as pd
from utm import from_latlon


class DataKey:
    def __init__(
        self,
        ghi_columns: list[str] | None = None,
        dhi_columns: list[str] | None = None,
        dni_columns: list[str] | None = None,
        poa_columns: list[str] | None = None,
        rhi_columns: list[str] | None = None,
        albedo_columns: list[str] | None = None,
        soiling_columns: list[str] | None = None,
        ambient_temperature_columns: list[str] | None = None,
        wind_speed_columns: list[str] | None = None,
        wind_direction_columns: list[str] | None = None,
        relative_humidity_columns: list[str] | None = None,
        pressure_columns: list[str] | None = None,
        rain_columns: list[str] | None = None,
        snow_columns: list[str] | None = None,
        tracker_angle_columns: list[str] | None = None,
        tracker_set_points_columns: list[str] | None = None,
        inverter_generation_columns: list[str] | None = None,
        power_factor_columns: list[str] | None = None,
        setpoint_columns: list[str] | None = None,
        meter_generation_columns: list[str] | None = None,
    ):

        # set irradiance data
        self.ghiColumns = ghi_columns
        self.dhiColumns = dhi_columns
        self.dniColumns = dni_columns
        self.rhiColumns = rhi_columns
        self.poaColumns = poa_columns
        self.albedoColumns = albedo_columns

        # set other weather data
        self.temperatureColumns = ambient_temperature_columns
        self.windSpeedColumns = wind_speed_columns
        self.windDirectionColumns = wind_direction_columns
        self.relativeHumidityColumns = relative_humidity_columns
        self.pressureColumns = pressure_columns
        self.rainColumns = rain_columns
        self.snowColumns = snow_columns

        # system data
        self.trackerAngleColumns = tracker_angle_columns
        self.trackerSetPointsColumns = tracker_set_points_columns
        self.inverterGenerationColumns = inverter_generation_columns
        self.powerFactorColumns = power_factor_columns
        self.setPointColumns = setpoint_columns
        self.meterGenerationColumns = meter_generation_columns

        # TODO: deal with blank lists instead of None


class Data:
    def __init__(
            self,
            file_path: str,
            header_row: int, # indexed from 0
            data_start_row: int, # indexed from 0
            nan_values: float | int | str,
            units_row: int | None = None, # indexed from 0
            delimiter: str | None = ','
            ):
        # read in data as dataframe
        self.df = pd.read_csv(
            file_path,
            delimiter=delimiter,
            header=None,
            na_values=nan_values
            )
        if units_row is not None:
            self.units = self.df.iloc[units_row]
        self.df.columns = self.df.iloc[header_row]
        self.df = self.df.iloc[data_start_row:]

        # remove columns if column name is nan
        keep_cols = [i for i in self.df.columns if not pd.isna(i)]
        self.df = self.df[keep_cols]

        # TODO: make tools for different time stamp inputs (single column format/multicolum)
        # TODO: deal with time zones (probably make everything UTC)
        # TODO: deal with interval starting/interval ending
        pass


class DataSet:
    def __init__(
            self,
            data_id: str,
            lat: float,
            lon: float,
            elevation: float | None,
            ):
        self.id = data_id
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
        easting, northing, zone, letter = from_latlon(lat, lon)
        self.easting = easting
        self.northing = northing
        self.utm_zone = zone
        self.magnetic_declination = geomag.declination(lat, lon)
        self.Data: Data | None = None

    def has_data(self) -> bool:
        return self.Data is not None

    def add_data(self, filepath: str, data_key: DataKey = None, source: str = "windog", time_shift: int = 0):
        self.Data = Data(filepath, data_key, source, time_shift)
        print("Data added to: " + self.id + "!")


if __name__ == '__main__':
    filepath = r"C:\Users\Annalise\Downloads\878733_40.93_-88.74_2023.csv"
    header_row = 2
    data_start_row = 3
    units_row = 1
    delimiter = ','
    nan_values = 'NaN'
    do = Data(filepath, header_row, data_start_row, nan_values, units_row, delimiter)