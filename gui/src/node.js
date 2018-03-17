
export class node {
  constructor(x, y, name, min, max, op) {
    this.x = x;
    this.y = y;
    this.name = name;
    this.min = min;
    this.max = max;
    this.selected = false;
    this.output_product = op;
    this.is_subproduct = false;
  }


  set_position(x, y) {
    this.x = x;
    this.y = y;
  }
  

}
