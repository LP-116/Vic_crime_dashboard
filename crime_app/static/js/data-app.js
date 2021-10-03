// Function run on webpage load.
// This first function populates the dropdown menu with the list of suburbs.
function init() {

    d3.json("/suburbs").then((item) => {

        console.log(item)

        suburb_list = []

        for (var i in item) {
                suburb_list.push(item[i].suburb)
                }

        var dropdownMenu = d3.select("#myList");

        var dropdownNames = suburb_list;
        
        dropdownNames.forEach((item) => {
        dropdownMenu
            .append("option")
            .text(item)
            .property("value", item);

        });

    });
};

init()


// Functions used to make the filter table button appear as loading.
function startSpinner() {
    // Codde to make the spinner start
    $("#filter-btn").prop("disabled", true);
    $("#filter-btn").html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp Loading...`
    );
}

function stopSpinner() {
    // Code to make the spinner stop
    // (i.e., return the button to its original state)
    $("#filter-btn").prop("disabled", false);
    $("#filter-btn").html('Filter Table');
}


// Selecting the filter button.
var filterButton = d3.select("#filter-btn");

// On click of the filter button run the runfilter function.
filterButton.on("click", runFilter);


// Funtion to return table results based on the 
function runFilter() {

    // Once the button is clicked run the start spinner function.
    startSpinner()

    // Prevent automatic reload.
    d3.event.preventDefault();

    // Select the suburb in the dropdown box.
    var suburbElement = d3.select("#suburbSelect");
    
    var suburbValue = suburbElement.property("value");
    console.log(suburbValue);   

    // Select the year in the dropdown box.
    var yearElement = d3.select("#yearSelect");
    var yearValue = yearElement.property("value");
    console.log(yearValue);
    
    var tbody = d3.select("tbody");
    
    // Using the data_tab route.
    d3.json("/data_tab").then((data)=> {
        
        // Filter the results on suburb and year.
        var filteredData = data.filter(dataEntry => ((dataEntry.suburb === suburbValue) && dataEntry.year === parseInt(yearValue, 10)))

        console.log(filteredData);

        //  If there is no results, return text stating "no results for selected inputs".
        if (!filteredData.length) {

            console.log("No result")
    
            tbody.html("");
    
            tbody.text("No results for selected inputs.");
            stopSpinner()}
    
        // Else, populate the table with the filtereddata results.
        else {
        
        tbody.html("");
    
        filteredData.forEach((dataEntry) => {
    
            var row = tbody.append("tr");
    
            Object.values(dataEntry).forEach((value) => {
                row.append("td").text(value);
            });
        });

        // Stop the spinner once retrieval is complete.
        stopSpinner()  

    }

});

}






