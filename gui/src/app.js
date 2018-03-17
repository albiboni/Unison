import "./stylesheets/main.css";

// Small helpers you might want to keep
import "./helpers/context_menu.js";
import "./helpers/external_links.js";

// ----------------------------------------------------------------------------
// Everything below is just to show you how it works. You can delete all of it.
// ----------------------------------------------------------------------------

var node_list = [], link_list = [], product_list = [], machines_list, external_suppliers_list, graph_list;
var product_json;
var selected_item = null;
var data_json = {product:{}, machines:{}, external_suppliers:{}, graph:{}};

import { node } from "./node";
import { link } from "./link";

import { product } from "./product";
import { machines} from "./machines";
import { external_suppliers} from "./external_suppliers";
import { grapth } from "./graphs";

import { update_settings, update_item_values } from "./settings_menu";  // TODO: Update this

// import {ImportJSON} from "./read_json";
// import {ExportJSON} from "./write_json";
//
// var data_import = ImportJSON(node_list, link_list, product_list);
// node_list = data_import['node_list']; link_list = data_import['link_list']; product_list['product_list'];
// ExportJSON(node_list, link_list, product_list);

var canvas = document.getElementById("canvas");
canvas.addEventListener('click', function(e) {
  update_settings(selected_item);
});

document.querySelector(".c_input").addEventListener("input", function (e) {
  update_item_values(selected_item);
});


// $("#export").click(function () {  // TODO: add button
//
//   for (new_product in product_list) {
//     data_json.product[new_product.name] = new_product;
//   }
//   for (new_machine in machines_list) {
//     data_json.machines[new_machine.name] = new_machine;
//   }
//   for (new_external in external_suppliers_list) {
//     data_json.machines[new_external.name] = new_external;
//   }
//   for (new_graph in graph_list) {
//     data_json.graphs[new_graph.name] = new_graph;
//   }
//
//   var fs = require("fs");
//   fs.writeFile("./object.json", JSON.stringify(data_json, null, 4), (err) => {
//     if (err) {
//         console.error(err);
//         return;
//     };
//     console.log("File has been created");
// });
// });

canvas.style.height = window.innerHeight;



