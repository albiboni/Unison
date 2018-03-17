import "./stylesheets/main.css";

// Small helpers you might want to keep
import "./helpers/context_menu.js";
import "./helpers/external_links.js";

// ----------------------------------------------------------------------------
// Everything below is just to show you how it works. You can delete all of it.
// ----------------------------------------------------------------------------

var node_list = []
var links = [];
var selected_item = null;
var node_width = { x: 170, y: 100 };

var strength = 1.0;


var scale = 1;
var scale_dx = 0.01;

var ingannt = false;


var drag = false;
var drag_index = 0;
var drag_delta = { x: 0, y: 0 };
var key, pressed;

import { node } from "./node";
import { link } from "./link";
import { update_settings, update_item_values } from "./settings_menu";


var canvas = document.getElementById("canvas");
canvas.addEventListener('click', function(e) {
  update_settings(selected_item);

  //let bound = canvas.getBoundingClientRect();

  //let x = e.clientX - bound.left - canvas.clientLeft - node_width.x/2;
  //let y = e.clientY - bound.top - canvas.clientTop - node_width.y/2;

  //node_list.push(new node(x, y, 'teste', 100, 1));

});

canvas.addEventListener('mousewheel', function (e) {
  console.log(e.wheelDelta)
  if (e.wheelDelta > 0) {
    scale = 1 + scale_dx;
  } else if (e.wheelDelta < 0) {
    scale = 1 - scale_dx;
  }
    context.scale(scale, scale)
 
});


document.getElementById('is_subproduct').addEventListener('change', function (e) {
  if (this.checked == true) {
    $(function () {
      $(".c_input").attr("disabled", true);
      document.getElementById("node_name").disabled = false;
    })
  } else {
    $(".c_input").attr("disabled", false);
  } 
});

document.querySelector(".create_node_button").addEventListener('click', function (e) {
  node_list.push(new node(300, 300, '', 0, 100, ''));
});

document.querySelector(".update_node_button").addEventListener('click', function (e) {
  update_item_values(selected_item);
});

document.querySelector(".update_link_button").addEventListener('click', function (e) {
  update_item_values(selected_item);
});

document.querySelector(".delete_node_button").addEventListener('click', function (e) {
  delete_selected_item();
});

document.querySelector(".delete_link_button").addEventListener('click', function (e) {
  delete_selected_item();
});

document.querySelector(".optimize_graph").addEventListener('click', function (e) {
  //send_graph();
});

document.querySelector(".gannt").addEventListener('click', function (e) {
  show_gannt_chart();
});

function show_gannt_chart() {
  ingannt = true;
  document.querySelector(".blur").style.display = 'block';

  google.charts.load('current', { 'packages': ['timeline'] });
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var container = document.getElementById('timeline');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    dataTable.addColumn({ type: 'string', id: 'President' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([
      ['Washington', new Date(1789, 3, 30), new Date(1797, 2, 4)],
      ['Adams', new Date(1797, 2, 4), new Date(1801, 2, 4)],
      ['Jefferson', new Date(1801, 2, 4), new Date(1809, 2, 4)]]);

    var options = {
      width: 800
    }
    chart.draw(dataTable, options);
  }
}



document.addEventListener('keydown', function (event) {
key = event.key; // "a", "1", "Shift", etc.
if (key == ';') {
  node_list.push(new node(100, 100, '', 0, 100, ''));
} else if (key == '/') {
  delete_selected_item();
} else if (key == 'Escape') {
  ingannt = false;
  document.querySelector(".blur").style.display = "none";
}
pressed = true;
  
});


function delete_selected_item() {
  if (selected_item instanceof link) {
    links.splice(links.indexOf(selected_item), 1);
    
  } else if (selected_item instanceof node) {
    for (var index = 0; index < links.length; index++) {
      if (links[index].connected_to === selected_item || links[index].connected_from === selected_item) {
        links.splice(index, 1);
        index--;
      }
    }
    node_list.splice(node_list.indexOf(selected_item), 1);
  } else {

  }

  }


document.addEventListener('keyup', function (e) {
  pressed = false;
});

canvas.addEventListener("mousedown", function (e) {
  let bound = canvas.getBoundingClientRect();

  let x = e.clientX - bound.left - canvas.clientLeft;
  let y = e.clientY - bound.top - canvas.clientTop;

  for (var index = node_list.length - 1; index >= 0; index--) {

    if ((x >= node_list[index].x) && x <= node_list[index].x + node_width.x && y >= node_list[index].y && y <= node_list[index].y + node_width.y) {

      if (key == 'Control' && selected_item !== node_list[index] && pressed == true) {
        links.push(new link(selected_item, node_list[index]));
      }

      
      try {
        selected_item.selected = false;
      } catch (err) { }

      drag_delta.x = x - node_list[index].x;
      drag_delta.y = y - node_list[index].y;

      drag = true;
      drag_index = index;

      selected_item = node_list[index]
      selected_item.selected = true;
      return;
    }
  }

  for (var index = links.length - 1; index >= 0; index--) {
    var tox = links[index].connected_to.x + node_width.x/2;
    var toy = links[index].connected_to.y + node_width.y/2;
    var fromx = links[index].connected_from.x + node_width.x / 2;
    var fromy = links[index].connected_from.y + node_width.y / 2;

    var xc = x - (tox + fromx) / 2;
    var yc = y - (toy + fromy) / 2;
    var length = Math.sqrt(Math.pow(toy - fromy, 2) + Math.pow(tox - fromx, 2));

    var angle = -Math.atan2(toy - fromy, tox - fromx);

    var xc_c = Math.cos(angle) * xc - Math.sin(angle) * yc;
    var yc_c = Math.sin(angle) * xc + Math.cos(angle) * yc;

    console.log(length / 2, 40);
    console.log({ x: xc_c, yc_c });


    if (Math.abs(xc_c) < length / 2 && Math.abs(yc_c) < 40) {
      console.log('test')
      try {
        selected_item.selected = false;
      } catch (err) { }
      selected_item = links[index]
      selected_item.selected = true;
      return;

    }

  }


  try {
    selected_item.selected = false;
  } catch (err) { }
  selected_item = null;

 

});

canvas.addEventListener("mousemove", function (e) {
  let bound = canvas.getBoundingClientRect();

  let m_x = e.clientX - bound.left - canvas.clientLeft;
  let m_y = e.clientY - bound.top - canvas.clientTop;

  if (drag) {

    node_list[drag_index].set_position(m_x - drag_delta.x, m_y - drag_delta.y);
  }

})

canvas.addEventListener('mouseup', function (e) {
  if (drag) {
    drag = false;
  }
});



canvas.style.height = window.innerHeight;
canvas.width = canvas.clientWidth;
canvas.height = canvas.clientHeight;

window.addEventListener('resize', function (event) {
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;

});


var context = canvas.getContext('2d', { alpha: false });
var origin_x = 0;
var origin_y = 0;

function update() {
}

function render() {
  clear_screen();
  render_links();
  render_nodes();

}

function clear_screen() {
  context.fillStyle = "white";
  context.fillRect(0, 0, canvas.width, canvas.height);
}

function render_nodes() {
     
  context.beginPath();
  context.strokeStyle = "black";
  for (var index = 0; index < node_list.length; index++) {

    if (node_list[index].selected == true) {
      context.fillStyle = "#cccccc";
    } else if (node_list[index].is_subproduct == true) {
      context.fillStyle = "lightgreen";
    }else {
      context.fillStyle = "#ffffff";
    }


    context.fillRect(node_list[index].x, node_list[index].y, node_width.x, node_width.y);
    context.rect(node_list[index].x, node_list[index].y, node_width.x, node_width.y);
      context.fillStyle = "#000000"
      context.font = "20px Arial";
      context.fillText(node_list[index].name, node_list[index].x + node_width.x / 4, node_list[index].y + node_width.y / 2);
    if (node_list[index].is_subproduct != true) {
      context.fillStyle = "#000000"
      context.font = "13px Arial";
      context.fillText("Max: " + node_list[index].max, node_list[index].x + 2, node_list[index].y + 13);
      context.fillText("Min: " + node_list[index].min, node_list[index].x + 2, node_list[index].y + node_width.y - 2);
    }
    
      
  }
  context.stroke();
  context.closePath();

}

function render_links() {
  context.fillStyle = "#000000"
  context.font = "20px Arial";
  context.strokeStyle = 'black';
  for (var index = 0; index < links.length; index++) {
    if (links[index].selected == true) {
      context.strokeStyle = 'red';
    } else {
      context.strokeStyle = 'black';
    }
    canvas_arrow(context, links[index].connected_from, links[index].connected_to);
    context.stroke();


  }

}

function canvas_arrow(context, node1, node2) {
  var fromx = node1.x + node_width.x / 2;
  var fromy = node1.y + node_width.y / 2;
  var tox = node2.x + node_width.x / 2;
  var toy = node2.y + node_width.y / 2;
  var headlen = 15;   // length of head in pixels
  var angle = Math.atan2(toy - fromy, tox - fromx);
  var radius = Math.sqrt(Math.pow(node_width.x/2,2) + Math.pow(node_width.y/2,2));
  context.moveTo(fromx + Math.cos(angle)*radius, fromy + Math.sin(angle)*radius);
  context.lineTo(tox - Math.cos(angle)*radius, toy - Math.sin(angle)*radius);
  context.lineTo(tox - Math.cos(angle) * radius - headlen * Math.cos(angle - Math.PI / 6), toy - Math.sin(angle) * radius - headlen * Math.sin(angle - Math.PI / 6));
  context.moveTo(tox - Math.cos(angle) * radius, toy - Math.sin(angle) * radius);
  context.lineTo(tox - Math.cos(angle) * radius - headlen * Math.cos(angle + Math.PI / 6), toy - Math.sin(angle) * radius - headlen * Math.sin(angle + Math.PI / 6));
  context.fillText(node1.output_product, (fromx + tox)/2, (toy + fromy)/2); 

}

function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

var frame = function (now) {
  update();
  render();
  requestAnimationFrame(frame, canvas);
};

frame();
