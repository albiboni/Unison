export class graphs {
  constructor(node_from, node_to, delay) {
    this.connected_from = node_from;
    this.connected_to = node_to;
    this.delay = delay;
  }

  set_delay(delay) {
    this.delay = delay;
  }

}
