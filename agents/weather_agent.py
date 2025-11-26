from typing import Dict, Any, List
import requests


CITY_COORDINATES: Dict[str, Dict[str, float]] = {
    "Paris": {
        "latitude": 48.8566,
        "longitude": 2.3522,
    }
}


def fetch_daily_weather_for_city(
    city_name: str,
    forecast_days: int = 2,
) -> Dict[str, Any]:
    """
    Récupère une prévision météo quotidienne simple pour une ville donnée
    en utilisant l'API Open-Meteo.
    """
    if city_name not in CITY_COORDINATES:
        raise ValueError(f"La ville {city_name} n'est pas supportée pour le moment.")

    coordinates = CITY_COORDINATES[city_name]

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "daily": "temperature_2m_max,precipitation_sum",
        "forecast_days": forecast_days,
        "timezone": "auto",
    }

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=params,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    daily_data = data.get("daily", {})

    return daily_data


def summarize_weather_for_swimming(
    city_name: str,
    forecast_days: int = 2,
) -> Dict[str, Any]:
    
    daily_data = fetch_daily_weather_for_city(city_name, forecast_days=forecast_days)

    dates: List[str] = daily_data.get("time", [])
    max_temps: List[float] = daily_data.get("temperature_2m_max", [])
    precipitations: List[float] = daily_data.get("precipitation_sum", [])

    details: List[Dict[str, Any]] = []

    good_days_count = 0

    for index, date_str in enumerate(dates):
        max_temp = max_temps[index]
        precipitation = precipitations[index]

        if precipitation > 2.0:
            status = "pluie"
        elif max_temp >= 24 and precipitation <= 1.0:
            status = "ensoleillé"
            good_days_count += 1
        else:
            status = "nuageux"

        details.append(
            {
                "date": date_str,
                "status": status,
                "max_temp_c": round(max_temp),
            }
        )

    if good_days_count >= 1:
        swimming_recommendation = "OK"
    else:
        swimming_recommendation = "Moyen"

    summary: Dict[str, Any] = {
        "location": city_name,
        "swimming_recommendation": swimming_recommendation,
        "details": details,
    }

    return summary
