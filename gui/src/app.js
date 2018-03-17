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


var canvas = document.getElementById("canvas");
canvas.addEventListener('click', function(e) {
  update_settings(selected_item);
});

document.querySelector(".c_input").addEventListener("input", function (e) {
  update_item_values(selected_item);
});

canvas.style.height = window.innerHeight;



