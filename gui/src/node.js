
export class node {
  constructor(x, y, name, min, max, is_on, output_rate, op) {
    this.x = x;
    this.y = y;
    this.name = name;
    this.min_output_rate = min;
    this.max_output_rate = max;
    this.output_rate = output_rate;
    this.is_on = is_on;
    this.output_product = op;
    this.output_product_units = '';
    this.selected = false;
    this.is_subproduct = false;
  }


  set_position(x, y) {
    this.x = x;
    this.y = y;
  }


}
