const BASE_URL = 'http://localhost:5000/api'
const searchResultsDiv = document.querySelector('#search-results')
const rescheduleSelectionBtn = document.querySelector('#select-reschedule')
const scheduleSelectionBtn = document.querySelector('#select-schedule')
const searchApptBtn = document.querySelector('#search-appt-btn')
const searchResultsUl = document.querySelector('#search-results')

async function handleApptSearch() {
    console.log('accessing handleApptSearch')
    const apptSearchQuery = document.querySelector('#search-appt').value
    console.log(apptSearchQuery)
    
    const res = await axios.get(`${BASE_URL}/reschedule/search`, {params: {q: apptSearchQuery}})

    for (let appt of res.data.appts) {
        let apptListing = document.createElement('li')
        apptListing.innerHTML = generateApptResultsHTML(appt)
        searchResultSection.append(apptListing)
    }
}

async function handleApptSelection(target) {
    if (target.tagname === 'LI') {
        let apptId = target.dataset.id

        const res = await axios.get(`${BASE_URL}/${apptId}/reschedule`)
    }
}

function generateApptResultsHTML(appt) {
    
    return `
        <li data-appt-id=${appt.id}>
            ${appt.title} / ${appt.start_time}
        </li>
    `
}

function toggleElementDisplay(element) {
    if (element.style.display === 'none') {
        element.style.display = 'block'
    } else {
        element.style.display = 'none'
    }
}


searchApptBtn.addEventListener('click', handleApptSearch)
rescheduleSelectionBtn.addEventListener('click', handleRescheduleSelection)
searchResultsUl.addEventListener('click', function(evt){handleApptSelection(evt.target)})