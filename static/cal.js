const BASE_URL = 'https://calendar-capstone.herokuapp.com'
const searchApptBtn = document.querySelector('#search-appt-btn')
const searchResultsUl = document.querySelector('#search-results')
const deleteApptBtn = document.querySelector('#delete-appt-btn')

// Helper Functions
function removeChild(parent) {
    while (parent.firstChild) {
        parent.firstChild.remove()
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
            <span><b><i>${appt.title}</i></b></span>  —  ${startDate.toDateString()} @ ${startTime12Hours}
            <a href=${BASE_URL}/${appt.id}/update>select</a>
        </li>
    `
}

async function getAppointments() {
    const apptSearchQuery = document.querySelector('#search-appt').value
    const res = await axios.get(`${BASE_URL}/api/reschedule/search`, {params: {q: apptSearchQuery}})
    
    return res
}

// Scheduling Functions

async function handleClientSearch() {
    const clientSearchQuery = document.querySelector('#search-client').value
    const res = await axios.get(`${BASE_URL}/api/reschedule/search`, {params: {q: clientSearchQuery}})

    if (res.data === 'not found') {
        flashApptNotFound()
    } else {
        for (let appt of res.data.appts) {
            let apptListing = document.createElement('li')
            apptListing.innerHTML = generateApptResultsHTML(appt)
            searchResultSection.append(apptListing)
        }
    }
}

//  Rescheduling Functions
async function handleApptSelection(target) {
    if (target.tagName === 'LI') {
        let apptId = target.dataset.apptId

        const res = await axios.get(`${BASE_URL}/${apptId}/update`)
    }
}

async function handleApptSearch() {
    removeChild(searchResultsUl)
    const res = await getAppointments()

    if (res.data.msg === 'not found') {
        flashApptNotFound()
    } else {
        for (let appt of res.data.appts) {
        
            let apptListing = document.createElement('li')
            apptListing.innerHTML = generateApptResultsHTML(appt)
            searchResultsUl.append(apptListing)
        }
    }
}

function flashApptNotFound() {
    let msg = document.createElement('p')
    msg.innerText = 'No Matching Appointments Found'
    searchResultsUl.append(msg)
}

// Event Listeners
searchResultsUl.addEventListener('click', function(evt){
    handleApptSelection(evt.target)
    })
searchApptBtn.addEventListener('click', handleApptSearch)