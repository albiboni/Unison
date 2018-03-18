import { node } from "./node";
import { link } from "./link";

var empty_settings = document.getElementById("empty_settings");
var node_settings = document.getElementById("node_settings");
var link_settings = document.getElementById("link_settings");

var node_name = document.getElementById("node_name");
var node_min_or = document.getElementById("node_min_or");
var node_max_or = document.getElementById("node_max_or");
var node_op = document.getElementById("node_op");
var node_op_units = document.getElementById("node_op_units");
var node_sp = document.getElementById("is_subproduct");
var node_io = document.getElementById("is_enabled");

var link_delay = document.getElementById("link_delay");
var link_amount = document.getElementById("link_amount");


export function update_settings(selected_item) {
  update_fields(selected_item);
  update_visibility(selected_item);

};

export function update_item_values(selected_item) {
  if (selected_item instanceof node) {
    selected_item.name = node_name.value;
    selected_item.min_output_rate = node_min_or.value;
    selected_item.max_output_rate = node_max_or.value;
    selected_item.output_product = node_op.value;
    selected_item.output_product_units = node_op_units.value;
    selected_item.is_subproduct = node_sp.checked;
    selected_item.is_on = node_io.checked;

  } else if (selected_item instanceof link) {
    selected_item.delay = link_delay.value;
    selected_item.amount = link_amount.value;
  } else {
  }

  return selected_item

}

function update_fields(selected_item) {
  if (selected_item instanceof node) {
    node_name.value = selected_item.name;
    node_min_or.value = selected_item.min_output_rate;
    node_max_or.value = selected_item.max_output_rate;
    node_op.value = selected_item.output_product;
    node_op_units.value = selected_item.output_product_units;
    node_sp.checked = selected_item.is_subproduct;
    node_io.checked = selected_item.is_on;

  } else if (selected_item instanceof link) {
    link_delay.value = selected_item.delay;
    link_amount.value = selected_item.amount;
  } else {
  }
  if (node_sp.checked == false) {
    $(".c_input").attr("disabled", false);
  } else {
    $(".c_input").attr("disabled", true);
    document.getElementById("node_name").disabled = false;}
  }


function update_visibility(selected_item) {
  if (selected_item instanceof node) {
    empty_settings.style.display = "none";
    link_settings.style.display = "none";
    node_settings.style.display = "inherit";
  } else if (selected_item instanceof link) {
    empty_settings.style.display = "none";
    link_settings.style.display = "inherit";
    node_settings.style.display = "none";
  } else {
    empty_settings.style.display = "inherit";
    link_settings.style.display = "none";
    node_settings.style.display = "none";
  }

}
