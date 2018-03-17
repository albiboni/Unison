export class link {
  constructor(node_from, node_to, delay) {
    this.connected_from = node_from;
    this.connected_to = node_to;
    this.delay = delay;
    this.selected = false;
    this.label = node_from.output_product;
    this.amount = 0;
  }

  set_delay(delay) {
    this.delay = delay;
  }

}
