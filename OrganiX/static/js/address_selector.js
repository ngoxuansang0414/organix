
const citiesDataBox = document.getElementById('cities-data-box')
const cityInput = document.getElementById('cities')


const districtsDataBox = document.getElementById('districts-data-box')
const districtInput = document.getElementById('districts')



const wardsDataBox = document.getElementById('wards-data-box')
const wardInput = document.getElementById('wards')



$.ajax({
    type: 'GET',
    url: "address/city",
    success: function (response) {
        const citiesData = response.data
        citiesData.map(item => {
            const option = document.createElement('option')
            
            option.textContent = item.name_with_type
            option.setAttribute('class', 'item')
            option.setAttribute('value', item.id)
            citiesDataBox.appendChild(option)  
        })
    },
    error: function (error) {
        console.log(error)
    }
})


cityInput.addEventListener('change', e => {
    const selectedCity = e.target.value

    districtsDataBox.innerHTML = ""

    $.ajax({
        type: 'GET',
        url: `address/${selectedCity}/districts`,
        success: function (response) {
            const districtsData = response.data
            const defaultOption = document.createElement('option')
            defaultOption.textContent = 'Chọn quận huyện'
            defaultOption.setAttribute('value', 0)
            districtsDataBox.appendChild(defaultOption)
            
            districtsData.map(item => {
                const option = document.createElement('option')    
                
                option.textContent = item.name_with_type               
                option.setAttribute('value', item.id)
                option.setAttribute('class', 'item')

                districtsDataBox.appendChild(option)
            })
        },
        error: function (error) {
            console.log(error)
        }
    })
        
})

districtInput.addEventListener('change', e => {
    const selectedDistrict = e.target.value

    wardsDataBox.innerHTML = ""

    $.ajax({
        type: 'GET',
        url: `address/${selectedDistrict}/wards`,
        success: function (response) {
            const wardsData = response.data
            const defaultOption = document.createElement('option')
            defaultOption.textContent = 'Chọn phường xã'
            defaultOption.setAttribute('value', 0)
            wardsDataBox.appendChild(defaultOption)
            wardsData.map(item => {
                const option = document.createElement('option')

                option.textContent = item.name_with_type
                option.setAttribute('value', item.id)
                option.setAttribute('class', 'item')

                wardsDataBox.appendChild(option)
            })
        },
        error: function (error) {
            console.log(error)
        }
    })
        
})

wardInput.addEventListener('change', e => {
})

