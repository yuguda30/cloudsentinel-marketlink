document.addEventListener("DOMContentLoaded", function () {
    const stateSelect = document.getElementById("stateSelect");
    const lgaSelect = document.getElementById("lgaSelect");

    if (!stateSelect || !lgaSelect) return;

    function loadLGAs(selectedLga = "") {
        const state = stateSelect.value;

        fetch(`/listing/lgas/${encodeURIComponent(state)}`)
            .then(res => res.json())
            .then(data => {
                lgaSelect.innerHTML = '<option value="">Select LGA</option>';

                data.forEach(lga => {
                    let option = document.createElement("option");
                    option.value = lga;
                    option.textContent = lga;

                    if (lga === selectedLga) {
                        option.selected = true;
                    }

                    lgaSelect.appendChild(option);
                });
            });
    }

    stateSelect.addEventListener("change", () => loadLGAs());

    const selected = lgaSelect.dataset.selected;
    if (selected) {
        loadLGAs(selected);
    }
});