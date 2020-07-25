d3.json("/api/v1.0/genre-count").then((genredata) => {
    var ctx = document.getElementById('genreBar').getContext('2d');
    var genreNames = Object.keys(genredata);
    var genreCount = Object.values(genredata);
    var color = Chart.helpers.color;
    console.log(genreCount); 
    console.log(genreNames);

    var data = {
        datasets: [{
            data: genreCount,
            label: "Genres",
            backgroundColor: ["rgb(45, 0, 247, 0.8)",
            "rgb(106, 0, 244, 0.8)",
            "rgb(137, 0, 242, 0.8)",
            "rgb(161, 0, 242, 0.8)",
            "rgb(177, 0, 232, 0.8)",
            "rgb(188, 0, 221, 0.8)",
            "rgb(209, 0, 209, 0.8)",
            "rgb(219, 0, 182, 0.8)",
            "rgb(229, 0, 164, 0.8)",
            "rgb(242, 0, 137, 0.8)"]
        }],
        labels: genreNames
        };

    var options = {
        title: {
            display: true,
            text: "Genre Count",
            fontColor : '#e500a4',
            fontSize: 24,
            fontStyle: 'normal',
            position: "top", 
            // events: ['click']
        },
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                gridLines: {
                    display: false
                }
                }]
        }
    };

    var mychart = new Chart(ctx, {
            data: data,
            type: 'bar',
            options: options
        });
});
    

d3.json("/api/v1.0/movie-info").then((countData) => {
    var ctx2 = document.getElementById("histogram").getContext('2d');
    var plotCountObject = {};
    // var plotCount = [];
    for(data of countData){
        // plotCount.push(countData["plot_word_count"])
        if (!plotCountObject[data["plot_word_count"]]){
            plotCountObject[data["plot_word_count"]] = 0    
        }
        plotCountObject[data["plot_word_count"]] += 1
    }
    console.log(plotCountObject);

    var countValues = Object.values(plotCountObject);
    var countLabels = Object.keys(plotCountObject);
    var plotChart = new Chart(ctx2, {
        type: 'bar',
        data: {
        labels: countLabels,
        datasets: [{
            label: 'Frequency of Plot Word Count',
            data: countValues,
            backgroundColor:'rgba(204, 255, 255, 0.5)'
        }]
        },
        options: {
        title: {
            display: true,
            text: "Frequency of Plot Word Count",
            fontColor : '#ffc5d2',
            fontSize: 24,
            fontStyle: 'normal',
            position: "top"
        },
        scales: {
            xAxes: [{
            display: true,
            barPercentage: 1.3,
            ticks: {
                max: 3,
            },
            gridLines: {
                display: false
            }
            }],
            yAxes: [{
            display: true,
            ticks: {
                beginAtZero:true
            },
            gridLines: {
                display: false
            }
            }]
        }
        }
    });

});

d3.select(".genre-btn").on("click", function(){
    var plotString = d3.select( ".plot-input" ).node().value;
    var plotObject = {
        plot: plotString
    }
    d3.json('/api/v1.0/genre-json', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body:  JSON.stringify(plotObject)
    }).then(function(response){
        console.log(response);

        d3.select('#alertZone').html(
        `<div class="alert alert-dismissible alert-secondary">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            ${response.response}
        </div>`
        )
    }).catch(function (err) {
        console.log(err, '<--error-->');

        d3.select('#alertZone').html(
        `<div class="alert alert-dismissible alert-danger">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
           Please enter a plot value
        </div>`
        )
    });
}
);
