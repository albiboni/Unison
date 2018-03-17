
export class node {
  constructor(name, min, max) {
    this.name = name;
    this.min = min;
    this.max = max;
    this.links = [];
  }


  add_link(link) {
    this.links.push(link);
  }

}
