import { product } from "./product";
import { machines } from "./machines";
import { external_suppliers} from "./external_suppliers"
import { graphs } from "./graphs"

export function ExportJSON(node_list, link_list, product_list) {
  var export_product = {};
  var export_graphs = [];
  var export_machines = {};
  var export_external_suppliers = {};

  for (var idx =0; idx < link_list.length; idx++) {
    export_graphs.push([(link_list[idx].connected_from.is_subproduct) ? "supplier of " + link_list[idx].connected_from.name : link_list[idx].connected_from.name,
    link_list[idx].connected_to.name,
    link_list[idx].delay]);
  }

  for (idx=0; idx < node_list.length; idx++) {
    if (node_list[idx].is_subproduct === true) {
      export_external_suppliers["supplier of " + node_list[idx].name] = {
        "min_batch_time": node_list[idx].min_output_rate,
        "max_batch_time": node_list[idx].max_output_rate,
        "batch_size": 20,
        "batch_time": node_list[idx].output_rate,
        "output_product": node_list[idx].name
      }
    }
    else {
      export_machines[node_list[idx].name] = {
        "min_batch_time": node_list[idx].min_output_rate,
        "max_batch_time": node_list[idx].max_output_rate,
        "batch_size": 20,
        "batch_time": node_list[idx].output_rate,
        "is_on": node_list[idx].is_on,
        "output_product": node_list[idx].output_product
      }
    }

  }

  var data = {
    "products": export_product,
    "machines": export_machines,
    "external_suppliers": export_external_suppliers,
    "graphs": export_graphs
  };


  return JSON.stringify(data)
};
//  fs.writeFile("./object.json", , (err) => {
//    if (err) {
//        console.error(err);
//        return;
//    };
//    console.log("File has been created");
//});


