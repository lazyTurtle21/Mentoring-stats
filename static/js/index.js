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

const renderPage = async () => {
    let data = await getData('v1');
    console.log(data);
};

renderPage();