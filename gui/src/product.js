
export class product {
  constructor(name, units, sub_product) {
    this.name = name;
    this.units = units;
    this.sub_product = sub_product;
  }

  add_subproduct(new_sub_product) {
    this.sub_product[new_sub_product.name] = new_sub_product.value;
  }

  set_name(name) {
    this.name = name;
  }

  set_units(units) {
    this.units = units;
  }

  set_subproduct(sub_product) {
    this.sub_product = sub_product;
  }
}
