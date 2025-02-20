import requests

url = "https://weatherapi-com.p.rapidapi.com/current.json"

city_name = input("Введите название города: ")
city = {"q":city_name}

headers = {
	"x-rapidapi-key": "6d91170cc5msh225dae2269b1fa4p1f32e5jsn93c87a393fbd",
	"x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=city)
temperature =  response.json()['current']['temp_c']
cloud = response.json()['current']['cloud']
wind = response.json()['current']['wind_kph']
print(f"В городе {city_name} сейчас температура равна {temperature}°C\nскорость ветра {wind} км/ч\nоблачность {cloud}%")
