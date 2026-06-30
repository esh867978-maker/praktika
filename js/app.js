const form = document.querySelector(".top-banner form");
const input = document.querySelector(".top-banner form input");
const msg = document.querySelector(".top-banner form .msg");
const list = document.querySelector(".ajax-section .cities");

const STORAGE_KEY = "weatherAppCities";
const ICON_BASE = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/162656";

function getApiKey() {
  return window.APP_CONFIG?.apiKey || "";
}

function loadSavedCities() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  } catch {
    return [];
  }
}

function saveCities(cities) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(cities));
}

function buildCityMarkup(data) {
  const { main, name, sys, weather } = data;
  const icon = `${ICON_BASE}/${weather[0].icon}.svg`;
  const cityKey = `${name},${sys.country}`;

  return `
    <h2 class="city-name" data-name="${cityKey}">
      <span>${name}</span>
      <sup>${sys.country}</sup>
    </h2>
    <div class="city-temp">${Math.round(main.temp)}<sup>°C</sup></div>
    <figure>
      <img class="city-icon" src="${icon}" alt="${weather[0].main}">
      <figcaption>${weather[0].description}</figcaption>
    </figure>
    <div class="city-actions">
      <button type="button" class="btn-remove" data-city="${cityKey}">Удалить</button>
    </div>
  `;
}

function appendCityCard(data) {
  const li = document.createElement("li");
  li.classList.add("city");
  li.innerHTML = buildCityMarkup(data);
  list.appendChild(li);

  li.querySelector(".btn-remove").addEventListener("click", () => {
    removeCity(`${data.name},${data.sys.country}`);
    li.remove();
  });
}

function removeCity(cityKey) {
  const cities = loadSavedCities().filter((c) => c.key !== cityKey);
  saveCities(cities);
}

function addCityToStorage(data) {
  const cityKey = `${data.name},${data.sys.country}`;
  const cities = loadSavedCities();
  if (!cities.find((c) => c.key === cityKey)) {
    cities.push({ key: cityKey, data });
    saveCities(cities);
  }
}

function isDuplicateCity(inputVal) {
  const listItems = list.querySelectorAll(".city");
  const listItemsArray = Array.from(listItems);

  if (listItemsArray.length === 0) {
    return false;
  }

  let searchVal = inputVal;

  const filteredArray = listItemsArray.filter((el) => {
    let content = "";

    if (searchVal.includes(",")) {
      if (searchVal.split(",")[1].length > 2) {
        searchVal = searchVal.split(",")[0];
        content = el.querySelector(".city-name span").textContent.toLowerCase();
      } else {
        content = el.querySelector(".city-name").dataset.name.toLowerCase();
      }
    } else {
      content = el.querySelector(".city-name span").textContent.toLowerCase();
    }

    return content === searchVal.toLowerCase();
  });

  if (filteredArray.length > 0) {
    const cityName = filteredArray[0].querySelector(".city-name span").textContent;
    msg.textContent = `You already know the weather for ${cityName} ...otherwise be more specific by providing the country code as well 😉 `;
    form.reset();
    input.focus();
    return true;
  }

  return false;
}

async function fetchWeather(cityName) {
  const apiKey = getApiKey();

  if (!apiKey) {
    throw new Error("API key is not configured");
  }

  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(cityName)}&appid=${apiKey}&units=metric`;

  const response = await fetch(url);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || "City not found");
  }

  return data;
}

async function searchWeather(inputVal) {
  if (isDuplicateCity(inputVal)) {
    return;
  }

  form.classList.add("loading");
  msg.textContent = "";

  try {
    const data = await fetchWeather(inputVal);
    appendCityCard(data);
    addCityToStorage(data);
    msg.textContent = "";
    form.reset();
    input.focus();
  } catch (error) {
    if (error.message === "API key is not configured") {
      msg.textContent = "API key не настроен. Проверьте переменную OPENWEATHER_API_KEY.";
    } else {
      msg.textContent = "Please search for a valid city 😩 ";
    }
  } finally {
    form.classList.remove("loading");
  }
}

function restoreSavedCities() {
  const cities = loadSavedCities();
  cities.forEach(({ data }) => appendCityCard(data));
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const inputVal = input.value.trim();

  if (!inputVal) {
    msg.textContent = "Введите название города.";
    return;
  }

  searchWeather(inputVal);
});

restoreSavedCities();
