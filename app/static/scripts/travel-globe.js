const visitedCountries = [
    { name: "Hungary", lat: 47.16, lng: 19.50 },
    { name: "Greece", lat: 39.07, lng: 21.82 },
    { name: "Germany", lat: 51.17, lng: 10.45 },
    { name: "Russia", lat: 61.52, lng: 105.32 },
    { name: "Ukraine", lat: 48.38, lng: 31.17 },
    { name: "Canada", lat: 56.13, lng: -106.35 },
    { name: "China", lat: 35.86, lng: 104.20 },
    { name: "US", lat: 39.83, lng: -98.58 },
];

const globeElement = document.getElementById("travel-globe");

if (globeElement && window.Globe) {
    const globe = new Globe(globeElement)
        .globeImageUrl("https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg")
        .backgroundColor("rgba(0, 0, 0, 0)")
        .pointsData(visitedCountries)
        .pointLat("lat")
        .pointLng("lng")
        .pointAltitude(0.03)
        .pointRadius(0.24)
        .pointColor(() => "#ff5a5f")
        .htmlElementsData(visitedCountries)
        .htmlLat("lat")
        .htmlLng("lng")
        .htmlElement(country => {
            const label = document.createElement("div");
            const dot = document.createElement("span");
            const text = document.createElement("span");

            label.className = "globe-label";
            dot.className = "globe-label-dot";
            text.className = "globe-label-text";
            text.textContent = country.name;

            label.appendChild(dot);
            label.appendChild(text);
            return label;
        })
        .htmlElementVisibilityModifier((label, isVisible) => {
            label.style.opacity = isVisible ? "1" : "0";
        });

    const resizeGlobe = () => {
        globe.width(globeElement.clientWidth);
        globe.height(globeElement.clientHeight);
    };

    resizeGlobe();
    window.addEventListener("resize", resizeGlobe);

    globe.pointOfView({ lat: 35, lng: 20, altitude: 1.8 });
    globe.controls().autoRotate = true;
    globe.controls().autoRotateSpeed = 0.6;
    globe.controls().enableZoom = false;
}
