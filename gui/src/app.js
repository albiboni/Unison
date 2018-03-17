import "./stylesheets/main.css";

// Small helpers you might want to keep
import "./helpers/context_menu.js";
import "./helpers/external_links.js";

// ----------------------------------------------------------------------------
// Everything below is just to show you how it works. You can delete all of it.
// ----------------------------------------------------------------------------

var node_list, links;
var selected_item = null;


import { node } from "./node";
import { link } from "./link";
import { update_settings, update_item_values } from "./settings_menu";

google.charts.load('current', {'packages': ['timeline']});
google.charts.setOnLoadCallback(drawChart);
// This defines the function format somehow
var format = require('string-format');

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length === 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
  return "#" + componentToHex(Math.floor(r*255/100)) + componentToHex(Math.floor(g*255/100)) + componentToHex(Math.floor(b*255/100));
}

function drawChart() {
  var schedule = require('../../core/Optimized_plant').schedule;

  var data = new google.visualization.DataTable();
  data.addColumn({type: 'string', id: 'row_label'});
  data.addColumn({type: 'string', id: 'bar_label'});
  data.addColumn({type: 'string', id: 'Style', role: 'style'});
  data.addColumn({type: 'number', id: 'Start'});
  data.addColumn({type: 'number', id: 'End'});


  for (var i = 0; i < schedule.length; i++) {
    var row = schedule[i];
    data.addRow([row[0],
      "capacity " + row[3].toFixed(1) + "%",
      format("color: rgb({0}, {1}, 0)", Math.floor(50+2*row[3]), Math.floor(255 - 2*row[3])),
      row[1] * 1000,
      row[2] * 1000]);
  }

  var options = {
    width: 700,

    height: 700
  };

  var chart = new google.visualization.Timeline(document.getElementById('chart_div'));
  chart.draw(data, options);
}
