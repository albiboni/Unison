import { product } from "./product";
import { machines } from "./machines";
import { external_suppliers} from "./external_suppliers"
import { graphs } from "./graphs"

export function ExportJSON(node_list, link_list, product_list) {
  var export_product = {};
  var export_machines = {};
  var export_external_suppliers = {};
  var export_graphs = [];


  for (var idx in product_list) {
    export_product[product_list[idx].name] = {"units":product_list[idx].units, "sub_products": product_list[idx].sub_product};
  }

  for (var idx in link_list) {
    export_graphs.push(([link_list[idx].is_subproduct) ? "supplier_" + link_list[idx].connected_from.name : link_list[idx].connected_from.name,
                        link_list[idx].connected_to.name,
                        link_list[idx].delay]);
  }

  for (var idx in node_list) {
    if (node_list[idx].is_subproduct == true) {
      export_external_suppliers["supplier_of_" + node_list[idx].name] = {
        "min_output_rate": node_list[idx].min_output_rate,
        "max_output_rate": node_list[idx].max_output_rate,
        "output_rate": node_list[idx].output_rate,
        "output_product":node_list[idx].name
      }
    }
    else {
      export_machines[node_list[idx].name] = {
        "min_output_rate": node_list[idx].min_output_rate,
        "max_output_rate": node_list[idx].max_output_rate,
        "output_rate": node_list[idx].output_rate,
        "is_on": node_list[idx].is_on,
        "output_product":node_list[idx].output_product
      }
    }

  }

  var data = {
    "products" : export_product,
    "machines" : export_machines,
    "external_suppliers" : export_external_suppliers,
    "graphs": export_graphs};


  return JSON.stringify(data);
//  fs.writeFile("./object.json", , (err) => {
//    if (err) {
//        console.error(err);
//        return;
//    };
//    console.log("File has been created");
//});

}
