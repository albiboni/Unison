import { node } from "./node";
import { link } from "./link";
import { product} from "./product"

export function ImportJSON(json_response, node_list, link_list, product_list) {
  var json_data = json_response; // TODO: Change path
  for (var connection in json_data.graph) {
    var input_name = json_data.graph[connection][0];
    var output_name = json_data.graph[connection][1];
    var upd_inp = update_node_list(input_name, node_list, json_data);
    node_list = upd_inp['node_list']; var input_node = upd_inp['new_node'];
    var upd_out = update_node_list(output_name, node_list, json_data);
    node_list = upd_out['node_list']; var output_node = upd_out['new_node'];
    link_list.push(new link(input_node, output_node, json_data.graph[connection][2]));
  }
  for (var new_product in json_data.products) {
    product_list.push(new product(new_product,
                                  json_data.products[new_product]['units'],
                                  json_data.products[new_product]['sub_products']))
  }
  alert(link_list.length);
  alert(node_list.length);
  alert(product_list.length);

  return {'node_list':node_list, 'link_list': link_list, 'product_list': product_list};
}

function update_node_list(parameter_name, node_list, json_data) {
  var exists_input = (node_list.map(x => x.name).indexOf(parameter_name) > -1);
  if (exists_input === false) {
    if (Object.keys(json_data.machines).indexOf(parameter_name) > -1) {
      var new_node = new node(
        (canvas.width/4)* (node_list.length % 4),
        ~~(node_list.length/4)*(canvas.height/4),
        parameter_name,
        json_data.machines[parameter_name]["min_batch_time"],
        json_data.machines[parameter_name]["max_batch_time"],
        json_data.machines[parameter_name]["is_on"],
        json_data.machines[parameter_name]["batch_time"],
        json_data.machines[parameter_name]["output_product"]);
    }
    else {
      var new_node = new node(
        (canvas.width/4)* (node_list.length % 4),
        ~~(node_list.length/4)*(canvas.height/4),
        parameter_name,
        json_data.external_suppliers[parameter_name]["min_batch_time"],
        json_data.external_suppliers[parameter_name]["max_batch_time"],
        null,
        json_data.external_suppliers[parameter_name]["batch_time"],
        json_data.external_suppliers[parameter_name]["output_product"]);
    }
    node_list.push(new_node);
  }
  else {
    new_node = node_list[node_list.map(x => x.name).indexOf(parameter_name)];
  }
  return {'node_list': node_list, 'new_node': new_node};
}

export function ImportJSON_response(json_reposnse, node_list) {
  for (var machine in json_reposnse.machines) {
    var idx = node_list.map(x => x.name).indexOf(machine);
    node_list[idx].output_rate = json_reposnse.machines[machine]["output_rate"];
  }
  for (var sup in json_reposnse.external_suppliers) {
    var short_name = sup.substring('supplier of '.length,);
    var idx = node_list.map(x => x.name).indexOf(short_name);
    node_list[idx].output_rate = json_reposnse.external_suppliers[sup]["batch_time"];
  }
  return node_list;
}
