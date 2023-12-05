import math
import os
import requests

class TileSystem:
    EarthRadius = 6378137
    MinLatitude = -85.05112878
    MaxLatitude = 85.05112878
    MinLongitude = -180
    MaxLongitude = 180

    @staticmethod
    def clip(n, minValue, maxValue):
        """
        Clips a number to the specified minimum and maximum values.

        Parameters:
        n (float): The number to clip.
        minValue (float): Minimum allowable value.
        maxValue (float): Maximum allowable value.

        Returns:
        float: The clipped value.
        """
        return max(min(n, maxValue), minValue)

    @staticmethod
    def map_size(level_of_detail):
        """
        Determines the map width and height (in pixels) at a specified level of detail.

        Parameters:
        level_of_detail (int): Level of detail, from 1 (lowest detail) to 23 (highest detail).

        Returns:
        int: The map width and height in pixels.
        """
        return 256 << level_of_detail

    @staticmethod
    def ground_resolution(latitude, level_of_detail):
        """
        Determines the ground resolution (in meters per pixel) at a specified latitude and level of detail.

        Parameters:
        latitude (float): Latitude (in degrees) at which to measure the ground resolution.
        level_of_detail (int): Level of detail, from 1 (lowest detail) to 23 (highest detail).

        Returns:
        float: The ground resolution, in meters per pixel.
        """
        latitude = TileSystem.clip(latitude, TileSystem.MinLatitude, TileSystem.MaxLatitude)
        return math.cos(latitude * math.pi / 180) * 2 * math.pi * TileSystem.EarthRadius / TileSystem.map_size(level_of_detail)

    @staticmethod
    def map_scale(latitude, level_of_detail, screen_dpi):
        """
        Determines the map scale at a specified latitude, level of detail, and screen resolution.

        Parameters:
        latitude (float): Latitude (in degrees) at which to measure the map scale.
        level_of_detail (int): Level of detail, from 1 (lowest detail) to 23 (highest detail).
        screen_dpi (int): Resolution of the screen, in dots per inch.

        Returns:
        float: The map scale, expressed as the denominator N of the ratio 1 : N.
        """
        return TileSystem.ground_resolution(latitude, level_of_detail) * screen_dpi / 0.0254

    @staticmethod
    def lat_long_to_pixel_xy(latitude, longitude, level_of_detail):
        """
        Converts a point from latitude/longitude WGS-84 coordinates (in degrees) into pixel XY coordinates at a specified level of detail.

        Parameters:
        latitude (float): Latitude of the point, in degrees.
        longitude (float): Longitude of the point, in degrees.
        level_of_detail (int): Level of detail, from 1 (lowest detail) to 23 (highest detail).

        Returns:
        tuple: A tuple containing the X and Y coordinates in pixels.
        """
        latitude = TileSystem.clip(latitude, TileSystem.MinLatitude, TileSystem.MaxLatitude)
        longitude = TileSystem.clip(longitude, TileSystem.MinLongitude, TileSystem.MaxLongitude)

        x = (longitude + 180) / 360
        sin_latitude = math.sin(latitude * math.pi / 180)
        y = 0.5 - math.log((1 + sin_latitude) / (1 - sin_latitude)) / (4 * math.pi)

        map_size = TileSystem.map_size(level_of_detail)
        pixel_x = int(TileSystem.clip(x * map_size + 0.5, 0, map_size - 1))
        pixel_y = int(TileSystem.clip(y * map_size + 0.5, 0, map_size - 1))
        return pixel_x, pixel_y

    @staticmethod
    def pixel_xy_to_lat_long(pixel_x, pixel_y, level_of_detail):
        """
        Converts a pixel from pixel XY coordinates at a specified level of detail into latitude/longitude WGS-84 coordinates (in degrees).

        Parameters:
        pixel_x (int): X coordinate of the point, in pixels.
        pixel_y (int): Y coordinate of the point, in pixels.
        level_of_detail (int): Level of detail, from 1 (lowest detail) to 23 (highest detail).

        Returns:
        tuple: A tuple containing the latitude and longitude in degrees.
        """
        map_size = TileSystem.map_size(level_of_detail)
        x = (TileSystem.clip(pixel_x, 0, map_size - 1) / map_size) - 0.5
        y = 0.5 - (TileSystem.clip(pixel_y, 0, map_size - 1) / map_size)

        latitude = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
        longitude = 360 * x
        return latitude, longitude

    @staticmethod
    def pixel_xy_to_tile_xy(pixel_x, pixel_y):
        """
        Converts pixel XY coordinates into tile XY coordinates of the tile containing the specified pixel.

        Parameters:
        pixel_x (int): Pixel X coordinate.
        pixel_y (int): Pixel Y coordinate.

        Returns:
        tuple: A tuple containing the tile X and Y coordinates.
        """
        tile_x = pixel_x // 256
        tile_y = pixel_y // 256
        return tile_x, tile_y

    @staticmethod
    def tile_xy_to_pixel_xy(tile_x, tile_y):
        """
        Converts tile XY coordinates into pixel XY coordinates of the upper-left pixel of the specified tile.

        Parameters:
        tile_x (int): Tile X coordinate.
        tile_y (int): Tile Y coordinate.

        Returns:
        tuple: A tuple containing the pixel X and Y coordinates.
        """
        pixel_x = tile_x * 256
        pixel_y = tile_y * 256
        return pixel_x, pixel_y

    @staticmethod
    def tile_xy_to_quad_key(tile_x, tile_y, level_of_detail):
        """
        Converts tile XY coordinates into a QuadKey at a specified level of detail.

        Parameters:
        tile_x (int): Tile X coordinate.
        tile_y (int): Tile Y coordinate.
        level_of_detail (int): Level of detail, from 1 (lowest detail) to 23 (highest detail).

        Returns:
        str: A string containing the QuadKey.
        """
        quad_key = []
        for i in range(level_of_detail, 0, -1):
            digit = '0'
            mask = 1 << (i - 1)
            if (tile_x & mask) != 0:
                digit = chr(ord(digit) + 1)
            if (tile_y & mask) != 0:
                digit = chr(ord(digit) + 2)
            quad_key.append(digit)
        return ''.join(quad_key)

    @staticmethod
    def quad_key_to_tile_xy(quad_key):
        """
        Converts a QuadKey into tile XY coordinates.

        Parameters:
        quad_key (str): QuadKey of the tile.

        Returns:
        tuple: A tuple containing the tile X and Y coordinates and the level of detail.
        """
        tile_x = tile_y = 0
        level_of_detail = len(quad_key)
        for i in range(level_of_detail):
            mask = 1 << (level_of_detail - i - 1)
            if quad_key[i] == '0':
                continue
            elif quad_key[i] == '1':
                tile_x |= mask
            elif quad_key[i] == '2':
                tile_y |= mask
            elif quad_key[i] == '3':
                tile_x |= mask
                tile_y |= mask
            else:
                raise ValueError("Invalid QuadKey digit sequence.")
        return tile_x, tile_y, level_of_detail

import requests
import os

def get_quadkeys_for_region(bottom_left_lat, bottom_left_lon, top_right_lat, top_right_lon, zoom_level):
    bottom_left_pixel_x, bottom_left_pixel_y = TileSystem.lat_long_to_pixel_xy(bottom_left_lat, bottom_left_lon, zoom_level)
    top_right_pixel_x, top_right_pixel_y = TileSystem.lat_long_to_pixel_xy(top_right_lat, top_right_lon, zoom_level)

    bottom_left_tile_x, bottom_left_tile_y = TileSystem.pixel_xy_to_tile_xy(bottom_left_pixel_x, bottom_left_pixel_y)
    top_right_tile_x, top_right_tile_y = TileSystem.pixel_xy_to_tile_xy(top_right_pixel_x, top_right_pixel_y)

    quadkeys = []
    for tile_x in range(bottom_left_tile_x, top_right_tile_x + 1):
        for tile_y in range(top_right_tile_y, bottom_left_tile_y + 1):
            quadkey = TileSystem.tile_xy_to_quad_key(tile_x, tile_y, zoom_level)
            quadkeys.append(quadkey)

    return quadkeys

def save_images_for_quadkeys(quadkeys, directory, common_params):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for quadkey in quadkeys:
        tile_x, tile_y, level_of_detail = TileSystem.quad_key_to_tile_xy(quadkey)
        pixel_x, pixel_y = TileSystem.tile_xy_to_pixel_xy(tile_x, tile_y)
        lat_top_left, lon_top_left = TileSystem.pixel_xy_to_lat_long(pixel_x, pixel_y, level_of_detail)
        lat_bottom_right, lon_bottom_right = TileSystem.pixel_xy_to_lat_long(pixel_x + 255, pixel_y + 255, level_of_detail)

        image_title = f"map_{lat_bottom_right}_{lon_top_left}_{lat_top_left}_{lon_bottom_right}.jpg"
        file_path = os.path.join(directory, image_title)

        params = {
            **common_params,
            "mapArea": f"{lat_bottom_right},{lon_top_left},{lat_top_left},{lon_bottom_right}",
            "format": "jpeg"
        }
        base_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to get image at {lat_bottom_right}, {lon_top_left}, {lat_top_left}, {lon_bottom_right}: {response.status_code}")

# Example usage
bottom_left_lat = 39.7416667  # Replace with actual latitude
bottom_left_lon = -86.1833333  # Replace with actual longitude
top_right_lat = 39.7853 # Replace with actual latitude
top_right_lon = -86.1340  # Replace with actual longitude
zoom_level = 19
quadkeys = get_quadkeys_for_region(bottom_left_lat, bottom_left_lon, top_right_lat, top_right_lon, zoom_level)

common_params = {
    "mapSize": "500,500",
    "mapLayer": "Basemap,Buildings",
    "key": "Ain7kUv28hvUkTkX5QfhVU-J_rqqtZMk7lGZNjh_e0ivB3wxcJsR3tAHJVAr8ZdC"  # Replace with your Bing Maps API Key
}
directory = "D:/OSMTestingImagesZL19"
save_images_for_quadkeys(quadkeys, directory, common_params)
