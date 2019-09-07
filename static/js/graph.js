queue()
    .defer(d3.json, "/get_cars")
    .await(pieChart);

function pieChart(error, buildData){
    var ndx = crossfilter(buildData);
    var make_dim = ndx.dimension(dc.pluck('make'));
    var total_per_build = make_dim.group().reduceSum(dc.pluck('total'));

    dc.pieChart('#amount-of-makes')
        .height(185)
        .radius(150)
        .transitionDuration(1500)
        .dimension(make_dim)
        .group(total_per_build)
        .legend(dc.legend().x(95).y(0).gap(5));

    dc.renderAll();
}