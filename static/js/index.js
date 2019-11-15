const getJSON = async (link) => {
    return await fetch(link)
        .then((response) => response.json())
        .then((responseJson) => {
            return responseJson
        });
};

const getData = async (api_v) => {
    let href = window.location.href;
    let qm_index = href.indexOf('?');
    qm_index = qm_index === -1 ? href.length : qm_index;

    return await (getJSON('/api/' + api_v + href.slice(qm_index, href.length)));
};

const getTableRow = data => {
    const el = document.createElement("li");
    el.className = "Table__row";
    el.innerHTML = `
            <div class="Column Column_name" data-label="Mentor"><b>${data.surname}</b></div>
            <div class="Column Column_hours" data-label="Hours">${data.hours}</div>
            <div class="Column Column_from" data-label="From">${data.from}</div>
            <div class="Column Column_to" data-label="To">${data.to}</div>
     `;
    return el;
};

const renderRows = async (container, data) => {
    if (Array.isArray(data) && data.length) {
        data.map(row_data => container.appendChild(getTableRow(row_data)));
    } else {
        container.appendChild(getTableRow(data));
    }
};


const renderPage = async () => {
    const table = document.querySelector(".Table");
    const data = await getData('v1');
    if (Object.entries(data).length === 0) {
        return;
    }
    const tableHeader = document.createElement('li');
    tableHeader.className = 'Table__header';
    tableHeader.innerHTML = `
            <div class="Column Column_name">Mentor's Surname</div>
            <div class="Column Column_hours">Hours Spent</div>
            <div class="Column Column_from">Date From</div>
            <div class="Column Column_to">Date To</div>
    `;
    table.appendChild(tableHeader);
    renderRows(table, data);
};


renderPage();