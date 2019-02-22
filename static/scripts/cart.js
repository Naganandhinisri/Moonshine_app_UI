
var shoppingCart = [];
    function displayShoppingCart(){
        var orderedProductsBody=document.getElementById("orderedProductsBody");
        while(orderedProductsBody.rows.length>0)
        {
            orderedProductsBody.deleteRow(0);
        }
        var cart_total_price=0;
        for(var product in shoppingCart){
            var row=orderedProductsBody.insertRow();
            var cellName = row.insertCell(0);
            var cellQuantity = row.insertCell(1);

            cellName.innerHTML = shoppingCart[product].Name;
            cellQuantity.innerHTML = shoppingCart[product].Quantity;

        }


    }


    function Add_to_cart(name,quantity)
    {
    var product = {};
    product.Name=name;
    product.Quantity=quantity;
    shoppingCart.push(product);
    displayShoppingCart();
    }
