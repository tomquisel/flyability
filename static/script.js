function render() {
}

function plotSummary(id, data) {
	$("#"+id).sparkline(toint(data), {type:"bar", chartRangeMin:0, chartRangeMax:100});
}

function plotFlyability(id, data) {
	opts = {}
	opts.type = "bar";
	opts.chartRangeMin = 0;
	opts.chartRangeMax = 100;
	opts.barWidth = '20';
	opts.height = '5em';
	$("#"+id).sparkline(toint(data), opts);
}

function plot(id, data) {
	opts = {}
	opts.type = "bar";
	opts.chartRangeMin = 0;
	opts.barWidth = '20';
	opts.height = '5em';
	$("#"+id).sparkline(toint(data), opts);
}

function toint(vals) {
	return $.map(vals, function(val, i) { return Math.round(val); });
}

function drawArrow(id, dir) {
	var canvas = $("#"+id).get(0);
	var context = canvas.getContext("2d");
	// this assumes it's a square.
	w = canvas.width;
	context.clearRect(0,0,w,w);
	pad = 1;
	angle = dir * Math.PI / 180.0;
	c = w / 2;
	halflen = w / 2 - pad;
	incx = halflen * -Math.sin(angle);
	incy = halflen * Math.cos(angle);
	fromx = c - incx;
	fromy = c - incy;
	tox = c + incx;
	toy = c + incy;
	context.beginPath();
	context.lineWidth = 3;
	canvasArrow(context,fromx, fromy, tox, toy);
	context.stroke();
}

function canvasArrow(context, fromx, fromy, tox, toy){
    var headlen = 10;   // length of head in pixels
    var angle = Math.atan2(toy-fromy,tox-fromx);
    context.moveTo(fromx, fromy);
    context.lineTo(tox, toy);
    context.lineTo(tox-headlen*Math.cos(angle-Math.PI/6),toy-headlen*Math.sin(angle-Math.PI/6));
    context.moveTo(tox, toy);
    context.lineTo(tox-headlen*Math.cos(angle+Math.PI/6),toy-headlen*Math.sin(angle+Math.PI/6));
}
