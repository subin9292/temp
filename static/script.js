document.addEventListener("DOMContentLoaded", () => {
    const currentWeather = {
        temp: "22.9°C",
        low: "18°C",
        high: "26°C",
        icon: "☀️"
    };

    document.getElementById('current-temp').textContent = currentWeather.temp;
    document.querySelector('.low-temp').textContent = currentWeather.low;
    document.querySelector('.high-temp').textContent = currentWeather.high;
    document.querySelector('.weather-icon').textContent = currentWeather.icon;

    const cities = [
        { name: "백령도", temp: "17°C", icon: "☁️", x: "10%", y: "5%" },
        { name: "서울", temp: "23°C", icon: "☀️", x: "42%", y: "22%" },
        { name: "춘천", temp: "21°C", icon: "⛅", x: "52%", y: "18%" },
        { name: "강릉", temp: "24°C", icon: "🌧️", x: "70%", y: "25%" },
        { name: "울릉/독도", temp: "24°C", icon: "🌧️", x: "85%", y: "18%" },
        { name: "수원", temp: "24.4°C", icon: "☀️", x: "43%", y: "28%" },
        { name: "청주", temp: "24°C", icon: "☀️", x: "48%", y: "36%" },
        { name: "대전", temp: "23.1°C", icon: "☀️", x: "45%", y: "45%" },
        { name: "안동", temp: "22.7°C", icon: "☀️", x: "55%", y: "35%" },
        { name: "대구", temp: "24.6°C", icon: "☀️", x: "56%", y: "55%" },
        { name: "전주", temp: "22.3°C", icon: "☀️", x: "35%", y: "48%" },
        { name: "광주", temp: "22.3°C", icon: "☀️", x: "35%", y: "56%" },
        { name: "목포", temp: "21.9°C", icon: "☀️", x: "30%", y: "65%" },
        { name: "여수", temp: "21.7°C", icon: "☀️", x: "42%", y: "70%" },
        { name: "울산", temp: "22.3°C", icon: "☀️", x: "72%", y: "60%" },
        { name: "부산", temp: "21.2°C", icon: "☀️", x: "68%", y: "68%" },
        { name: "제주도", temp: "23.1°C", icon: "☀️", x: "25%", y: "85%" }
    ];

    const mapElement = document.getElementById('map-overlay');

    cities.forEach(city => {
        const weatherElement = document.createElement('div');
        weatherElement.classList.add('weather-info');
        weatherElement.style.left = city.x;
        weatherElement.style.top = city.y;
        weatherElement.innerHTML = `
            <div class="icon">${city.icon}</div>
            <div class="name">${city.name}</div>
            <div class="temp">${city.temp}</div>
        `;
        mapElement.appendChild(weatherElement);
    });
});