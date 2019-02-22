var shoppingCart = [];
    function displayShoppingCart(){
        var orderedProductsBody=document.getElementById("orderedProductsBody");
        while(orderedProductsBody.rows.length>0)
        {
            orderedProductsBody.deleteRow(0);
        }

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
    var html = "<table border='1|1' >";
            html += "<td>NAME ID</td>";

            html += "<td>Quantity</td>";

            html += "<td>Action</td>";
            for (var i = 0; i <  shoppingCart.length; i++) {
                html += "<tr>";
                html += "<td>" +  shoppingCart[i].name_id + "</td>";

                html += "<td>" +  shoppingCart[i].product_qty + "</td>";

                html += "<td><button type='submit' onClick='deleteProduct(\"" +  shoppingCart[i].name_id + "\", this);'/>Delete Item</button> &nbsp <button type='submit' onClick='addCart(\"" +  shoppingCart[i].name_id + "\", this);'/>Add to Cart</button></td>";
                html += "</tr>";
            }
            html += "</table>";
            document.getElementById("demo").innerHTML = html;

            document.getElementById("resetbtn").click()
        }
        function deleteProduct(name_id, e) {
            e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
            for (var i = 0; i <  shoppingCart.length; i++) {
                if ( shoppingCart[i].name_id == name_id) {

                     shoppingCart.splice(i, 1);
                }
            }
        }

        function addCart(name_id) {

            for (var i = 0; i <  shoppingCart.length; i++) {
                if ( shoppingCart[i].name_id == name_id) {
                    var cartItem = null;
                    for (var k = 0; k < cart.length; k++) {
                        if (cart[k].product.name_id ==  shoppingCart[i].name_id) {
                            cartItem = cart[k];
                            cart[k].product_qty++;
                            break;
                        }
                    }
                    if (cartItem == null) {

                        var cartItem = {
                            product:  shoppingCart[i],
                            product_qty:  shoppingCart[i].product_qty
                        };
                        cart.push(cartItem);
                    }
                }
            }

            renderCartTable();

        }

        function renderCartTable() {
        var html = '';
        var ele = document.getElementById("demo2");
        ele.innerHTML = '';

        html += "<table id='tblCart' border='1|1'>";
        html += "<tr><td>NAME ID</td>";

        html += "<td>Quantity</td>";

        html += "<td>Total</td>";
        html += "<td>Action</td></tr>";
        var GrandTotal = 0;
        for (var i = 0; i < cart.length; i++) {
            html += "<tr>";
            html += "<td>" + cart[i].product.NAME_id + "</td>";

            html += "<td>" + cart[i].product_qty + "</td>";

            html += "<td>" + parseFloat(cart[i].product.product_price) * parseInt(cart[i].product_qty) + "</td>";
            html += "<td><button type='submit' onClick='subtractQuantity(\"" + cart[i].product.name_id + "\", this);'/>Subtract Quantity</button> &nbsp<button type='submit' onClick='addQuantity(\"" + cart[i].product.name_id + "\", this);'/>Add Quantity</button> &nbsp<button type='submit' onClick='removeItem(\"" + cart[i].product.name_id + "\", this);'/>Remove Item</button></td>";
            html += "</tr>";

           GrandTotal += parseFloat(cart[i].product.product_price) * parseInt(cart[i].product_qty);

        }
        document.getElementById('demo3').innerHTML = GrandTotal;
        html += "</table>";
        ele.innerHTML = html;
    }


        function subtractQuantity(product_id)
        {

            for (var i = 0; i < cart.length; i++) {
                if (cart[i].product.name_id == name_id) {
                    cart[i].product_qty--;
                }

                if (cart[i].product_qty == 0) {
                    cart.splice(i,1);
                }

            }
            renderCartTable();
        }
        function addQuantity(name_id)
        {

            for (var i = 0; i < cart.length; i++) {
                if (cart[i].product.name_id == name_id) {
                    cart[i].product_qty++;
                }
            }
            renderCartTable();
        }
        function removeItem(name_id)
        {

            for (var i = 0; i < cart.length; i++) {
                if (cart[i].product.name_id == name_id) {
                    cart.splice(i,1);
                }

            }
            renderCartTable();
    displayShoppingCart();
    }
