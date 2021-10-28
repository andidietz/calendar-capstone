const BASE_URL = 'http://localhost:5000'
const searchResultsDiv = document.querySelector('#search-results')
const rescheduleSelectionBtn = document.querySelector('#select-reschedule')
const scheduleSelectionBtn = document.querySelector('#select-schedule')
const searchApptBtn = document.querySelector('#search-appt-btn')
const searchResultsUl = document.querySelector('#search-results')

//  Rescheduling Functions
async function handleApptSearch() {
    const apptSearchQuery = document.querySelector('#search-appt').value
    const res = await axios.get(`${BASE_URL}/api/reschedule/search`, {params: {q: apptSearchQuery}})

    for (let appt of res.data.appts) {
        let apptListing = document.createElement('li')
        apptListing.innerHTML = generateApptResultsHTML(appt)
        searchResultsUl.append(apptListing)
    }
}

async function handleApptSelection(target) {
    console.log(target)
    console.log(target.dataset.apptId)

    if (target.tagName === 'LI') {
        let apptId = target.dataset.apptId

        const res = await axios.get(`${BASE_URL}/reschedule/${apptId}/update`)
    }
}

function turnStringToNums(datesAndTimes) {
    let valuesAsNums = []
    for(let value of datesAndTimes) {
        valuesAsNums.push(parseInt(value))
    }
    return valuesAsNums
}

function generateApptResultsHTML(appt) {
    const startDate = new Date(appt.start_date)

    const piecesofStartDate = appt.start_date.split('-')
    const sDate = turnStringToNums(piecesofStartDate)

    const piecesofStartTime = appt.start_time.split(':')
    const sTime = turnStringToNums(piecesofStartTime)

    const startTime12Hours = new Date(sDate[0], sDate[1], sDate[2], sTime[0], sTime[1]).toLocaleTimeString('en-US');

    return `
        <li data-appt-id='${appt.id}'>
            ${appt.title} / ${startDate.toDateString()}/ ${startTime12Hours}
            <a href=${BASE_URL}/reschedule/${appt.id}/update>select</a>
        </li>
    `
}

// Scheduling Functions

async function handleClientSearch() {
    const clientSearchQuery = document.querySelector('#search-client').value
    const res = await axios.get(`${BASE_URL}/api/reschedule/search`, {params: {q: clientSearchQuery}})

    for (let appt of res.data.appts) {
        let apptListing = document.createElement('li')
        apptListing.innerHTML = generateApptResultsHTML(appt)
        searchResultSection.append(apptListing)
    }
}

function toggleElementDisplay(element) {
    if (element.style.display === 'none') {
        element.style.display = 'block'
    } else {
        element.style.display = 'none'
    }
}

searchResultsUl.addEventListener('click', function(evt){
    handleApptSelection(evt.target)
    })
searchApptBtn.addEventListener('click', handleApptSearch)
rescheduleSelectionBtn.addEventListener('click', handleRescheduleSelection)