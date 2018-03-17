export class link {
  constructor(node_from, node_to) {
    this.connected_from = node_from;
    this.connected_to = node_to;
    this.delay = 0;
    this.selected = false;
    this.label = node_from.output_product;
  }

  set_delay(delay) {
    this.delay = delay;
  }

}
